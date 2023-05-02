# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
# from langchain.chains.question_answering import load_qa_chain
# from langchain.llms import OpenAI
# from chat import MovieChatBot

# movie = {"Overview": "Set more than a decade after the events of the first film learn the story of the Sully family (Jake Neytiri and their kids) the trouble that follows them the lengths they go to keep each other safe the battles they fight to stay alive and the tragedies they endure.",
# 		"Reviews":[
# 		"""*Shazam! Fury of the Gods remembered everything that made its predecessor so delightful and delivered a sequel as fun as the first!*\r\n\r\nShazam! Fury of the Gods matches the fun of the first film while, in typical sequel fashion, increasing the action, effects, and scope of the Shazam franchise. Despite being a Shazam movie, Freddy is the primary focus of the film, which I was unsure about at first but enjoyed as the story progressed. Fury of the Gods had many more characters to juggle, leading to some of the Shazam family being sidelined and the villains being reasonably stereotypical. However, all the charm was still there, helping overshadow these flaws. Djimon Hounsou and Helen Mirren brought some maturity and class to the goofball cast, and Zachary Levi was a blast, as always. If you enjoyed the first film, you will also love Fury of the Gods. It’s a bigger serving of all the delight, optimism, and horror-flavoring that made the original great.""",
# 		"""FULL SPOILER-FREE REVIEW @ https://www.firstshowing.net/2023/review-shazam-fury-of-the-gods-falls-into-the-typical-sequel-trap/\r\n\r\n\"Shazam! Fury of the Gods is almost saved by the incredibly charismatic, energetic cast, as well as by a truly thrilling third act. Unfortunately, the movie falls into the trap of exaggerating what worked in the original, excessively tackling every narrative aspect, and losing authenticity along the way. Way too long, boringly generic, and lacking a clearer direction, namely in the treatment of its family themes. Comedy is far from the efficiency of its predecessor. I recommend it to the vast majority of fans of the genre, who will certainly enjoy the lightness still present in this sequel.\"\r\n\r\nRating: C""",
# 		"""Ok, so I know I shouldn't have - but I did enjoy this. \"Billy\" (Zachary Levi/Asher Angel) and his gang of rather hapless super-heroes locally lauded as the \"Philadelphia Fiascos\" find themselves pushed to the very limits when the daughters of the legendary \"Atlas\" manage to breach a magical boundary between their world and our's and are soon on the hunt for the magical staff that \"Billy\" snapped in two at the end of the last film (remember?). The daughters are led by the menacing \"Hespera\" (Dame Helen Mirren) with her potent sidekick \"Kalypso\" (Lucy Liu) and the slightly more humane \"Anthea\" (Rachel Zegler) making up this dangerous triumvirate. What now ensues are some genuinely entertaining set piece battles that unlike so many from the MCU, are based on creatures from mythology and do not drag on interminably. Levi is as much an anti-hero as you can imagine, his tongue firmly in his cheek - though not so much as Dame Helen's - as he and his gang look hopelessly - and continuously - outgunned, outmanoeuvred and outwitted. Can they rally and save the day before carnage ensues and mankind is wiped out? Nope, not a shred of jeopardy here - but the two hours just flew by. It's fun. It's not trying to offer us any grand philosophies, or complex time-shifting science. It's a lightly comedic adventure film that rarely stops for breath, uses state of the art special effects to enhance the story rather than dominate it, and by the end I was ready to remember why I quite enjoyed the original from 2019. All of this said, I fear they will try to squeeze a third from the franchise and think that would be an error. This works because of some charismatic performances - particularly from the rather engaging Jack Dylan Grazer as the lovestruck \"Freddy\"; a great big dragon and an at times quite pithy script. Please let's leave well alone now?"""
# 		]}


# mb = MovieChatBot(movie)

# mb.preprocess()

# print(mb.ask_question("What is the movie about and what did the reviewers think of it?"))
# print(mb.ask_question("Who are the actors in the movie?"))

import requests

api_key = 'b5ae8f373afd12ae8115950d51b1306d'
query = 'Aveng'
url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=en-US&query={query}&page=1&include_adult=false'

array = []

for movie in requests.get(url).json()['results']:
	array.append(movie['id'])

print(array)