import streamlit as st
from streamlit_chat import message
import time
import requests
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from chat import MovieChatBot
from utils import get_movie_detail

api_key = 'b5ae8f373afd12ae8115950d51b1306d'

search_results = []


movie_query = st.text_input("Search a Movie", placeholder="Enter Movie Name")
url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=en-US&query={movie_query}&page=1&include_adult=false'

for movie in requests.get(url).json()['results']:
	search_results.append((movie['id'],movie['original_title']))

if search_results:
	selection = st.selectbox("Select Movie",options = search_results, format_func=lambda x:x[1])
st.write("Click start chat to initiate the conversation")
if st.button('Start Chat'):
	# data = get_movie_detail(selection[0])
	st.session_state.bot=None
	memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
	memory.save_context({"input":"Hello!"},{"output":f"Let's discuss about the movie {selection[1]} (tmdbID = {selection[0]})"})
	st.session_state.bot = MovieChatBot(selection,memory)

	cols = st.columns(2)
	data  = get_movie_detail(selection[0])
	with cols[0]:
		st.write(f"You can now start chatting with the bot about {selection[1]}")
	with cols[1]:	
		img = data['img']	
		st.image(img,width = 200)	

	st.title('Similar Movies')
	cols = st.columns(5)
	try:
		with cols[0]:
			st.image(data['recommendations'][0]['img_url'])
			st.write(data['recommendations'][0]['title'])
		with cols[1]:
			st.image(data['recommendations'][1]['img_url'])
			st.write(data['recommendations'][1]['title'])
		with cols[2]:
			st.image(data['recommendations'][2]['img_url'])
			st.write(data['recommendations'][2]['title'])
		with cols[3]:
			st.image(data['recommendations'][3]['img_url'])
			st.write(data['recommendations'][3]['title'])
		with cols[4]:
			st.image(data['recommendations'][4]['img_url'])
			st.write(data['recommendations'][4]['title'])
	except IndexError:
		pass

with st.sidebar:

	if 'bot' in st.session_state:

		new_msg = st.text_input("Send Message",placeholder="")
		
		if st.button("Send Message"):
			with st.spinner("Sending Message"):
				st.session_state.bot.ask_question(new_msg)

		for i, msg in enumerate(st.session_state.bot.memory.load_memory_variables({})['chat_history']):
			if i%2 == 0:
				message(message = msg.content,is_user=True)
			else:
				message(message = msg.content, is_user = False)	
			
			# message(message = msg["Content"],is_user=msg["is_user"], key = str(time.time()))

