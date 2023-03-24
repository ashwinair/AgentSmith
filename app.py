import streamlit as st
import pandas as pd
from io import StringIO
import openai
from api import OPENAI_API_KEY

st.set_page_config(page_title = 'this is title', page_icon = ':tada:', layout = 'wide')

st.markdown("<h1 style='text-align: center; color: grey;'>Talk to your CSV</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a file")
st.write(uploaded_file)

openai.api_key = OPENAI_API_KEY
#user_input = st.text_input("Enter your query here",  value= " ")

with st.form("Input"):
    user_input = st.text_area("Enter your query here:", height=5, max_chars=None)
    btnResult = st.form_submit_button('Run')

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()


    if btnResult:
        prompt = f'GET {user_input} from this csv file and ignore irrelevant data and check the data properly and dont discribe the answer: {bytes_data}'

        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
        st.write(response['choices'][0]["message"]["content"].strip())  

        # To convert to a string based IO:
        #stringio = StringIO(response['choices'][0]["message"]["content"].strip())
        # st.write(stringio)
        # To read file as string:
        # string_data = stringio.read()
        # st.write(string_data)
        print(response)
        # Can be used wherever a "file-like" object is accepted:
        #dataframe = pd.read_csv(stringio, sep=",", header=None)
        #st.write(dataframe)
