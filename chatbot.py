# chatbot.py
import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS

chain = None

def setup_chain(data):
    global chain
    embeddings = OpenAIEmbeddings()
    vectors = FAISS.from_documents(data, embeddings)
    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(temperature=0.0, model_name='gpt-3.5-turbo-16k'),
        retriever=vectors.as_retriever())

def conversational_chat(query):
    if chain is None:
        return "Chain is not initialized."

    result = chain({"question": query, "chat_history": st.session_state['history']})
    st.session_state['history'].append((query, result["answer"]))
    return result["answer"]
