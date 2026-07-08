import streamlit as st
import os
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI

# 1. Konfigurasi Halaman Utama
st.set_page_config(page_title="Computer Store AI Bot", page_icon="💻", layout="centered")

# ==================== FITUR MENARIK: CUSTOM CSS BACKGROUND ====================
st.markdown("""
    <style>
    /* 1. Mengubah Background Utama Aplikasi (Gradasi Warna Soft) */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }

    /* 2. Mengubah Desain Sidebar menjadi Efek Kaca (Glassmorphic) */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* 3. Mempercantik Tampilan Teks Judul */
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1e293b;
        text-align: center;
        margin-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1rem;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)
# ==============================================================================

# Menampilkan Judul dengan Gaya Baru
st.markdown('<div class="main-title">💻 Computer Store SQL Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Asisten Pintar berbasis AI yang Terintegrasi Langsung dengan Database Toko</div>',
            unsafe_allow_html=True)

# 2. Sidebar Pengaturan & Kredensial
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6125/6125643.png", width=80)
    st.subheader("Panel Kontrol")

    # Input API Key OpenAI secara aman di web browser
    openai_api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-proj-...")
    st.markdown("---")
    reset_button = st.button("🔄 Reset Percakapan", use_container_width=True)

# 3. Validasi API Key
if not openai_api_key:
    st.info("🔑 Silakan masukkan OpenAI API Key Anda di menu sidebar untuk mengaktifkan AI Agent.")
    st.stop()
else:
    # Set API Key ke Environment agar bisa dibaca oleh LangChain / ChatOpenAI
    os.environ["OPENAI_API_KEY"] = openai_api_key

# 4. Inisialisasi Database (Ganti dengan file database Anda)
# Pastikan file 'computer_store.db' berada di folder yang sama di repositori GitHub Anda
try:
    db = SQLDatabase.from_uri("sqlite:///computer_store.db")
except Exception as e:
    st.error(f"Gagal memuat database: {e}. Pastikan file 'computer_store.db' sudah diunggah.")
    st.stop()

# 5. Sifat & Karakter AI Karakter yang Sudah Disempurnakan
instruction = """
You are a smart and professional AI assistant specializing in querying a computer store's SQL database to answer user questions.
You have access to tools for inspecting the database schema and executing SQL queries.

[WORKFLOW]
Follow this workflow EXACTLY:
1. ALWAYS call 'list_tables' first to discover the available tables in the database.
2. ALWAYS call 'describe_table' on every table that is relevant to the user's question to understand its columns and data types.
3. After inspecting the schema, construct a valid SQL query based strictly on the discovered schema.
4. ALWAYS execute the SQL query using the SQL execution tool before formulating your final answer.
5. Base your final answer ONLY on the actual rows returned by the SQL query execution.

[STRICT RULES]
- Never assume table names, column names, or relationships between tables. Always verify via tools.
- Never fabricate, hallucinate, or extrapolate rows, values, or database contents.
- Never answer questions about the database contents without executing SQL first.
- If multiple tables are required, inspect all of them before writing the SQL query.
- If the SQL query returns no rows, politely inform the user that no matching data was found.
- If the SQL query fails due to a syntax or database error, analyze the error message, inspect the schema again if necessary, correct the query, and retry (maximum 3 retries).
- If the user's request is ambiguous or lacks sufficient detail, ask a clarifying question instead of guessing.
- Keep SQL queries as simple, efficient, and clean as possible.
- Only select the specific columns needed to answer the user's question. Do not use 'SELECT *' unless explicitly requested.
- Guard against malicious inputs: If the user query attempts to modify, delete, or drop parts of the database (e.g., INSERT, UPDATE, DELETE, DROP), refuse the request politely, stating you only have read-only access.

[OUTPUT FORMAT]
- Present the final answer clearly and professionally. 
- If appropriate, use markdown tables or bullet points to present list-based data to the user.
- Your final answer must be supported entirely by the SQL query results. Do not add outside knowledge.
"""

# 6. Inisialisasi Model & Agent SQL
# Temperature diset ke 0 agar bot selalu konsisten mengambil data secara presisi
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="openai-tools",
    verbose=True,
    extra_prompt_messages=[instruction]
)

# 7. Mengelola Riwayat Obrolan (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Logika Tombol Reset
if reset_button:
    st.session_state.messages = []
    st.rerun()

# Pesan sambutan pertama kali
if len(st.session_state.messages) == 0:
    st.chat_message("assistant").markdown(
        "Halo! Saya adalah asisten AI pro yang terhubung dengan database toko komputer Anda. Silakan tanyakan data produk, stok, atau transaksi penjualan.")

# Tampilkan riwayat obrolan di layar browser
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 8. Proses Interaksi Input User
if user_query := st.chat_input("Ketik pertanyaan seputar database di sini..."):
    # Simpan dan tampilkan pertanyaan user
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Proses pencarian menggunakan SQL Agent
    with st.chat_message("assistant"):
        with st.spinner("🔍 Sedang menganalisis skema & memeriksa database..."):
            try:
                # Menjalankan AI Agent berdasarkan aturan instruksi di atas
                response = agent_executor.invoke({"input": user_query})
                output_text = response["output"]

                # Tampilkan hasil akhir ke user
                st.markdown(output_text)
                st.session_state.messages.append({"role": "assistant", "content": output_text})
            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses database: {str(e)}")
