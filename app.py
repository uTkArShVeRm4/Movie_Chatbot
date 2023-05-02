import streamlit as st
from streamlit_chat import message
import time
import requests
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from chat import MovieChatBot
from utils import get_movie_detail

api_key = 'b5ae8f373afd12ae8115950d51b1306d'

search_results = []
widget_counter=0
if 'history' not in st.session_state:
    st.session_state.history = []	

if 'bot' not in st.session_state:
    st.session_state.bot = MovieChatBot()	


movie_query = st.text_input("Search a Movie", placeholder="")
url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=en-US&query={movie_query}&page=1&include_adult=false'

for movie in requests.get(url).json()['results']:
    search_results.append((movie['id'],movie['original_title']))

if search_results:
    selection = st.selectbox("Select Movie",options = search_results, format_func=lambda x:x[1])

if st.button('Start Chat'):
    data = get_movie_detail(selection[0])
    with st.spinner("Extracting movie data"):
        st.session_state.bot.preprocess(data)

    cols = st.columns(2)
    with cols[0]:
        st.write(f"You can now start chatting with the bot about {selection[1]}")
    with cols[1]:	
        st.image(data['img'],use_column_width=True)
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
        print('')
        
    st.session_state.history.clear()
 
     

with st.sidebar:

    new_msg = st.text_input("Send Message",placeholder="")
    
    if st.button("Send Message"):
        st.session_state.history.append({"Content": new_msg, "is_user":True})

        with st.spinner("Sending Message"):
            reply = st.session_state.bot.ask_question(new_msg)
        st.session_state.history.append({"Content": reply, "is_user":False})
    for i, msg in enumerate(st.session_state.history):
        if msg["Content"] == "":
            st.session_state.history.pop(i)
        widget_counter+=1
        key = f"{widget_counter}_{time.time()}"
        message(message = msg["Content"],is_user=msg["is_user"], key = key)
