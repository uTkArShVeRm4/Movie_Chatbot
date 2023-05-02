from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType, load_tools
from langchain.tools import BaseTool
from langchain.llms import OpenAI
from utils import search_wikipedia,scrape_wikipedia
import os

os.environ["OPENAI_API_KEY"] = "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"

class MovieChatAgent():

	def __init__(self):
		self.chatbot = MovieChatBot()
		self.llm = OpenAI(temperature=0)
		self.agent = None

	def preprocess_chatbot(self,data):
		self.chatbot.preprocess(data)	

	def get_from_wikipedia(self,query):
		return 	self.chatbot.add_info(scrape_wikipedia(search_wikipedia(query)[1]))

	# class FindWikiPediaInfo(BaseTool):
	# 	name = "Find Wiki Info"
	# 	description = "Use this tool to get information about anything/anyone from wikepedia and add it to the stored information. Use SendReply tool after to get the final reply to the question. Send the search item as the target"

	# 	def _run(self, query:str) -> str:
	# 		#Use tool
	# 		result = search_wikipedia("Avatar The Way of Water(2022)")
	# 		html = scrape_wikipedia(result[1])

	# 		self.add_info(html)
	# 		return 'Successfully Added info to database'

	# 	async def _arun(self, query: str) -> str:
	# 		raise NotImplementedError("Does not support async")	

	# class SendReply(BaseTool):
	# 	name = "Send Reply"
	# 	description = "Use this tool to send reply to the user question on a given movie. Use FindWikiPediaInfo if you require extra information. It queries the database and calculates the reply. Send the user question as it is in the query"
		
	# 	def _run(self, query:str) -> str:
	# 		return self.chatbot.ask_question(query)

	# 	async def _arun(self, query: str) -> str:
	# 		raise NotImplementedError("Does not support async")	

	def create_agent(self):
		self.tools = [
		Tool.from_function(
			func = self.get_from_wikipedia,
			name = "Find Wiki Info",
			description = "Use this tool to get information about anything/anyone from wikepedia and add it to the stored information. Use SendReply tool after to get the final reply to the question. Send the search item as the target"
			),
		Tool.from_function(
			func = self.chatbot.ask_question,
			name = "Send Reply",
			description = "Use this tool to answer movie related questions. Use FindWikiPediaInfo if you require extra information. It queries the database and calculates the reply. Send the user question as it is in the query"
			)
		]
		self.agent = initialize_agent(self.tools, self.llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose = True)     

class MovieChatBot():

	def __init__(self):
		self.data = None
		self.document = ""

	def preprocess(self,data):	
		self.data = data
		text_splitter = CharacterTextSplitter(        
		    separator = "\n",
		    chunk_size = 1000,
		    chunk_overlap  = 200,
		    length_function = len,
		)

		self.document += f"Overview : {self.data['Overview']}"

		for i, review in enumerate(self.data["Reviews"]):
			self.document += (f"Review {i+1}: "+ review)



		self.texts = text_splitter.split_text(self.document)


		self.embeddings = OpenAIEmbeddings()
		self.docsearch = FAISS.from_texts(self.texts, self.embeddings)
		self.chain = load_qa_chain(OpenAI(), chain_type="stuff")

	def add_info(self,data):

		text_splitter = CharacterTextSplitter(        
		    separator = "\n",
		    chunk_size = 1000,
		    chunk_overlap  = 200,
		    length_function = len,
		)

		self.document += (data)

		self.texts = text_splitter.split_text(self.document)

		self.embeddings = OpenAIEmbeddings()
		self.docsearch = FAISS.from_texts(self.texts, self.embeddings)
		self.chain = load_qa_chain(OpenAI(), chain_type="stuff")


	def ask_question(self,question):

		docs = self.docsearch.similarity_search(question)
		return self.chain.run(input_documents=docs, question=question)