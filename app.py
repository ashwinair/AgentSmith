import streamlit as st
import pandas as pd
from io import StringIO
import openai

st.set_page_config(page_title = 'Talk to your CSV', page_icon = ':male_mage:', layout = 'wide')

st.markdown("<h1 style='text-align: center; color: grey;'>Talk to your CSV</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a file",type=['csv'],accept_multiple_files=False,)

st.write(uploaded_file)

openai.api_key = st.secrets["OPENAI_API_KEY"]
#user_input = st.text_input("Enter your query here",  value= " ")

with st.form("Input"):
    user_input = st.text_area("Enter your query here:", height=5, max_chars=None)
    btnResult = st.form_submit_button('Run')


if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    if user_input.__len__() <= 10: #taking 10 just as testing purpose most of the query will contain more than 5 words (ofc)
        st.error('Input your query and start talking!', icon="❔")

    elif btnResult and user_input != ' ':
        prompt = f'find {user_input} from this csv file and give output in csv format with asked columns names, ignore irrelevant data and check the data properly and dont discribe the answer: {bytes_data}'
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])

        # To convert to a string based IO:
        stringio = StringIO(response['choices'][0]["message"]["content"].strip())
        # st.write(stringio)
        # To read file as string:
        # string_data = stringio.read()
        # st.write(string_data)
        print(response)
        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(stringio, sep=",", header=None)
        st.write(dataframe)
else:
    if btnResult:
        st.error('Upload your CSV file before start talking!', icon="🚨")

st.markdown("<h1 style='text-align: center; color: grey; font-size:30px'>👨‍💻 - <a href='https://github.com/ashwinair'>ashwinair</a></h1>", unsafe_allow_html=True)
