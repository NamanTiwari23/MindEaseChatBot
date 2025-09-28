import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq


def initialize_llm():
    llm = ChatGroq(
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY"),  # loaded from .env
        model_name="meta-llama/llama-4-scout-17b-16e-instruct"
    )
    return llm


def create_vector_db(db_path="chroma_db", data_path="data"):
    loader = DirectoryLoader(data_path, glob='*.pdf', loader_cls=PyPDFLoader)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    # Automatically persisted if you set persist_directory
    vector_db = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=db_path
    )

    # No need to call .persist() manually in newer versions
    return vector_db


def load_vector_db(db_path="chroma_db"):
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings)
    return vector_db

def setup_qa_chain(vector_db, llm):
    retriever = vector_db.as_retriever()

    prompt_template = """You are a compassionate mental health chatbot. Respond thoughtfully to the user's question based on the context below.
Context: {context}
User: {question}
Chatbot:"""

    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT}
    )
    return qa_chain

# This function will be called by your Flask app
def get_chatbot_response(user_query):
    if not hasattr(get_chatbot_response, "qa_chain"):
        llm = initialize_llm()

        db_path = "chroma_db"
        if not os.path.exists(db_path):
            vector_db = create_vector_db(db_path)
        else:
            vector_db = load_vector_db(db_path)

        get_chatbot_response.qa_chain = setup_qa_chain(vector_db, llm)

    return get_chatbot_response.qa_chain.invoke(user_query)

