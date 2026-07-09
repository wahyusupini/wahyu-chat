import streamlit as stop
import os
# Contoh menggunakan langchain (pastikan sudah pip install langchain langchain-community langchain-openai streamlit)
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI

# 1. Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Computer Store AI Bot", page_icon="💻")
st.title("💻 Computer Store SQL Assistant")

# 2. Inisialisasi Database & LLM (Sesuaikan URI database Anda)
# Anda bisa menggunakan SQLite untuk testing awal
db = SQLDatabase.from_uri("sqlite:///computer_store.db")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0) # Pastikan temperature 0 untuk SQL agar konsisten

# 3. Masukkan Instruction yang Sudah Disempurnakan
instruction = """
[Salin teks instruction yang sudah disempurnakan di atas ke sini]
"""

# 4. Membuat Agent SQL
agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="openai-tools",
    verbose=True,
    extra_prompt_messages=[instruction] # Memasukkan sifat bot ke dalam sistem
)

# 5. Interface Chat di Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Halo! Ada yang bisa saya bantu terkait data di toko komputer?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if user_query := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)
    
    with st.chat_message("assistant"):
        with st.spinner("Berpikir dan memeriksa database..."):
            try:
                # Jalankan agen AI
                response = agent_executor.invoke({"input": user_query})
                output_text = response["output"]
                
                st.write(output_text)
                st.session_state.messages.append({"role": "assistant", "content": output_text})
            except Exception as e:
                st.error(f"Terjadi kesalahan: {str(e)}")
