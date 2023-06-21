import streamlit as st
import pandas as pd
from io import StringIO
import openai

st.set_page_config(page_title = 'Talk to your CSV', page_icon = ':male_mage:', layout = 'wide')

st.markdown("<h1 style='text-align: center; color: grey;'>Talk to your CSV</h1>", unsafe_allow_html=True)
st.sidebar.header('Sidebar')
uploaded_file = st.sidebar.file_uploader("Choose a file",type=['csv'],accept_multiple_files=False,)

st.sidebar.write(uploaded_file)
container = st.container()
container.write("This is inside the container")
openai.api_key = "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"
#st.secrets["OPENAI_API_KEY"]


user_input = st.text_input("Enter your query here:")
#btnResult = st.form_submit_button('Run')


if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    if user_input.__len__() <= 10: #taking 10 just as testing purpose most of the query will contain more than 5 words (ofc)
        st.error('Input your query and start talking!', icon="❔")

    elif user_input:
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
        container.write(dataframe)
else:
    st.warning('Upload your CSV file before start talking!', icon="🚨")

st.sidebar.markdown("<h1 style='text-align: center; color: grey; font-size:20px'>👨‍💻 - <a href='https://github.com/ashwinair'>ashwinair</a></h1>", unsafe_allow_html=True)
