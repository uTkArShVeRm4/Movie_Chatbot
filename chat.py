from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI

from utils import query_wikipedia,get_movie_detail
import os

os.environ["OPENAI_API_KEY"] = ""


def ask_wiki(queryquestion):

	query,question = queryquestion.split('|')
	print(query,question)
	document = query_wikipedia(query)


	text_splitter = CharacterTextSplitter(        
		    separator = "\n",
		    chunk_size = 1000,
		    chunk_overlap  = 200,
		    length_function = len
		)


	texts = text_splitter.split_text(document)

	embeddings = OpenAIEmbeddings()
	docsearch = FAISS.from_texts(texts, embeddings)
	chain = load_qa_chain(OpenAI(), chain_type="stuff")
	docs = docsearch.similarity_search(question)
	return chain.run(input_documents=docs, question=question)


def movie_info(moviequestion):

	movie,question = moviequestion.split('|')

	data = get_movie_detail(movie)

	document = f"Overview : {data['Overview']}"
	for i, review in enumerate(bot.data["Reviews"]):
		document += (f"Review {i+1}: "+ review)

	text_splitter = CharacterTextSplitter(        
		    separator = "\n",
		    chunk_size = 1000,
		    chunk_overlap  = 200,
		    length_function = len,
		)


	texts = text_splitter.split_text(document)


	embeddings = OpenAIEmbeddings()
	docsearch = FAISS.from_texts(texts, embeddings)
	chain = load_qa_chain(OpenAI(), chain_type="stuff")
	docs = docsearch.similarity_search(question)
	return chain.run(input_documents=docs, question=question)


class MovieChatBot():

	def __init__(self,movie,memory):
		self.movie = movie
		self.tools = [
		Tool.from_function(
			func = ask_wiki,
			name = 'Query Wikipedia',
			description = "Useful for when you need to access new information about any movie/person or anyone else from wikipedia. Input to this function should be strictly in the format 'Target| question', where Target is the article from wikipedia to be searched and question is the question asked by user"
			),
		Tool.from_function(
			func = movie_info,
			name = "Movie user reviews",
			description = "Useful for when you are asked question about movies and user reviews of the movies. Input to this function should be strictly in the format'movieId| question', where movieId is the tmdbId of the movie and question is the question user asked about the movie."
			)
		]
		self.memory = memory

		self.llm=ChatOpenAI(temperature=0)
		self.agent_chain = initialize_agent(self.tools, self.llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)

	def ask_question(self,question):
		return self.agent_chain.run(question)	