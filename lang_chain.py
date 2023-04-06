from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import os

os.environ["OPENAI_API_KEY"] = "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"
#load document
loader = CSVLoader(file_path = 'Coursera_Course_List.csv')

# Create an index using the loaded documents
index_creator = VectorstoreIndexCreator()
docsearch = index_creator.from_loaders([loader])

# Create a question-answering chain using the index
chain = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", 
retriever=docsearch.vectorstore.as_retriever(), input_key="question")

#pass query

query = 'what is the roll no. of ashwin'
response = chain({'question':query})

print(response)
     
