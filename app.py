# app.py
import os
import streamlit as st
from streamlit_chat import message
from chatbot import conversational_chat, setup_chain
from pdf_loader import load_pdf_data

# OpenAI APIキーの入力
user_api_key = st.sidebar.text_input(
    label="OpenAI APIキー",
    placeholder="ここにOpenAI APIキーを貼り付けてください",
    type="password")

# PDFファイルのアップロード
uploaded_file = st.sidebar.file_uploader("ファイルをアップロード", type="pdf")

# 環境変数にAPIキーを設定
if user_api_key:
    os.environ['OPENAI_API_KEY'] = user_api_key

# PDFファイルがアップロードされた場合、データを読み込み
if user_api_key and uploaded_file is not None:
    data = load_pdf_data(uploaded_file)
    setup_chain(data)

# チャットボットの履歴を管理
if 'history' not in st.session_state:
    st.session_state['history'] = []

# 初期メッセージの設定
if 'generated' not in st.session_state:
    if uploaded_file is not None:
        st.session_state['generated'] = ["こんにちは！このドキュメントに関する質問があれば、何でもお尋ねください。"]
    else:
        st.session_state['generated'] = ["会話を始めるには、PDFファイルをアップロードしてください。"]

if 'past' not in st.session_state:
    st.session_state['past'] = ["やあ！"]

# チャットインターフェースの設定
response_container = st.container()
container = st.container()
with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_input("質問：", placeholder="PDFデータについてここで話しましょう :)", key='input')
        submit_button = st.form_submit_button(label='送信')

    if submit_button and user_input and user_api_key:
        output = conversational_chat(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
            message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")
