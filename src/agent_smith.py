import os
from io import StringIO
import re
import sys
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_toolkits import (
    create_vectorstore_agent,
    VectorStoreInfo,
    VectorStoreToolkit
)

from modules.layout import Layout
from modules.embedder import Embedder
import streamlit as st

layout = Layout()

layout.show_header()

st.sidebar.write("Upload your document here 📂:")
# from apis import openai_api_key
uploaded_file = st.sidebar.file_uploader(
    "upload", type=['pdf'], label_visibility="collapsed")
st.sidebar.write("Enter your OpenAI API KEY")
user_openai_api_key = st.sidebar.text_input(
    'OpenAI API key', type='password', placeholder= "sk -...............", key='api_key', label_visibility="collapsed")

os.environ['OPENAI_API_KEY'] = user_openai_api_key

if not user_openai_api_key:
    layout.show_api_key_missing()
elif user_openai_api_key == 'resume':
    os.environ['OPENAI_API_KEY'] = st.secrets["OPENAI_API_KEY"]
    
    # create instance of OpenAI LLM
    llm = ChatOpenAI(temperature=0.2,model_name='gpt-3.5-turbo')
    #OpenAI(model_name="gpt-3.5-turbo",temperature=0.1, verbose=True)

    embeds = Embedder()
    if uploaded_file:
        file = uploaded_file.read()
        # load documents into vector database (ChromaDB)
        vectorstore = embeds.getDocEmbeds(file, uploaded_file.name)

        # create vectorstore info object - matadata repo
        vectorstore_info = VectorStoreInfo(
            name=uploaded_file.name,
        description='a stock annual report as a pdf',
        vectorstore=vectorstore
        )

        # Convert the Document store into a langchain toolkit
        toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)

        # add the toolkit to an end-to-end LC
        agent_executor = create_vectorstore_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True
        )

        # create a text input box for the user
        # Display the prompt form

        is_ready, agent_mode, prompt = layout.prompt_form(uploaded_file)
        #  = st.text_input(label='Input your questions here....')

        # pass the prompt to LLm
        if is_ready:
            if agent_mode:

                # Create a StringIO object to capture the output
                output_buffer = StringIO()

                # Replace sys.stdout with the output buffer
                sys.stdout = output_buffer

                try:
                    response = agent_executor.run(prompt)
                except: 
                    st.warning('Please provide a Valid API key')

                # capture agents thoughts and observation
                thoughts = output_buffer.getvalue()

                # Restore sys.stdout to its original value
                sys.stdout = sys.__stdout__

                # Clean up the agent's thoughts to remove unwanted characters
                cleaned_thoughts = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', thoughts)
                cleaned_thoughts = re.sub(r'\[1m>', '', cleaned_thoughts)
                # Display the agent's thoughts
                st.code(cleaned_thoughts)
            else:
                try:
                    response = agent_executor.run(prompt)
                except: 
                    st.warning('Please provide a Valid API key')
                thoughts = response
                # write the response
                st.write('Final Response: {response}')

            # find the revelant pages of the response
            with st.expander("Document Similarity Search"):
                search = vectorstore.similarity_search_with_score(prompt)
                st.write(search[0][0].page_content)
    else:
        st.warning("Upload your files to Search 🚨")
