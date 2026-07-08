import streamlit as st
from google import genai
from google.genai import types
import time

# 1. Konfigurasi Halaman Utama 🚀
st.set_page_config(page_title="Gemini SQL Chatbot Pro", page_icon="💻", layout="centered")

# ==================== FITUR PREMIUM: CUSTOM CSS BACKGROUND & JAM NEON TERANG ====================
st.markdown("""
    <style>
    /* 1. Mengembalikan Background Utama Aplikasi ke Gradasi Semula (Soft & Clean) 🎨 */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%) !important;
    }
    
    /* 2. Mengubah Desain Sidebar menjadi Efek Kaca (Glassmorphic) 🔮 */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* 3. FITUR KEREN: Judul Bergerak Melayang & Berubah Warna 🌈 */
    @keyframes floatAndGlow {
        0% { transform: translateY(0px); background-position: 0% 50%; }
        50% { transform: translateY(-8px); background-position: 100% 50%; }
        100% { transform: translateY(0px); background-position: 0% 50%; }
    }

    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
        background: linear-gradient(270deg, #2563eb, #9333ea, #3b82f6, #06b6d4);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: floatAndGlow 4s ease-in-out infinite;
    }
    
    .moving-pc {
        display: inline-block;
        animation: pcRotateBounce 3s ease-in-out infinite;
    }
    
    @keyframes pcRotateBounce {
        0% { transform: scale(1) rotate(0deg); }
        25% { transform: scale(1.15) rotate(5deg); }
        50% { transform: scale(1) rotate(-5deg); }
        75% { transform: scale(1.15) rotate(3deg); }
        100% { transform: scale(1) rotate(0deg); }
    }
    
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1rem;
        margin-bottom: 25px;
    }
    
    /* 4. Animasi Bergerak Muncul pada Balon Chat 💬 */
    @keyframes chatPopUp {
        0% { opacity: 0; transform: translateY(20px) scale(0.98); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }

    [data-testid="stChatMessage"] {
        animation: chatPopUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    /* 5. Kustomisasi & Animasi Karakter Avatar (User & Bot) 🧑‍💻 */
    @keyframes avatarBreath {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-4px); }
        100% { transform: translateY(0px); }
    }

    [data-testid="stChatMessage"] img[src*="user"] {
        content: url("https://cdn-icons-png.flaticon.com/512/4140/4140037.png") !important;
        border-radius: 50%;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
        animation: avatarBreath 3s ease-in-out infinite;
    }
    
    [data-testid="stChatMessage"] img[src*="assistant"] {
        content: url("https://cdn-icons-png.flaticon.com/512/8943/8943377.png") !important;
        border-radius: 50%;
        box-shadow: 0px 4px 10px rgba(37, 99, 235, 0.3);
        animation: avatarBreath 3s ease-in-out infinite;
        animation-delay: 1.5s;
    }

    [data-testid="stChatMessage"]:hover img {
        transform: scale(1.25) rotate(12deg);
        transition: transform 0.4s ease;
    }
    
    /* 6. GAYA JAM SUPER TERANG BISA DIBACA ⏰ */
    .time-badge {
        font-size: 0.8rem;
        font-weight: 800;
        color: #ffffff !important;
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%) !important;
        padding: 3px 10px !important;
        border-radius: 6px !important;
        display: inline-block !important;
        margin-top: 8px !important;
        box-shadow: 0px 3px 8px rgba(59, 130, 246, 0.5) !important;
    }
    </style>
""", unsafe_allow_html=True)
# ==============================================================================

# Menampilkan Judul Dinamis 🌟
st.markdown('<div class="main-title"><span class="moving-pc">💻</span> Gemini SQL Chatbot Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Database Agent • Jam Lokal Indonesia Akurat • Kaya Emotikon ✨</div>', unsafe_allow_html=True)

# 2. Sidebar Pengaturan ⚙️
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6125/6125643.png", width=80) 
    st.subheader("Panel Kontrol 🛠️")
    google_api_key = st.text_input("Google AI API Key", type="password", placeholder="Masukkan API Key Anda...")
    
    st.markdown("---")
    st.subheader("🔊 Opsi Suara Realistis")
    enable_voice = st.checkbox("Aktifkan Suara Bot (Auto-Speak)", value=False)
    
    # 10 Pilihan Profil Suara Realistis 🗣️
    voice_character = st.selectbox(
        "Pilih Agen Suara Realistis:",
        [
            "👩 Sari (Suara Utama - Lembut & Natural)",
            "👩 Dian (Eksekutif - Formal & Profesional)",
            "👩 Nadia (Customer Service - Ramah & Cepat)",
            "👩 Amalia (Presenter - Jelas & Berirama)",
            "👩 Citra (Gaya Santai - Akrab & Logat Kota)",
            "👨 Budi (Suara Utama - Berat & Karismatik)",
            "👨 Andika (Narator - Tegas & Berwibawa)",
            "👨 Rendi (Teknisi Toko - Cepat & Energetik)",
            "👨 Gunawan (Manajer - Tenang & Bijaksana)",
            "👨 Fajar (Gaya Santai - Casual & Friendly)"
        ]
    )
    
    st.markdown("---")
    reset_button = st.button("🔄 Reset Percakapan", use_container_width=True)

# Parameter suara manusia asli 🎯
voice_params = {
    "👩 Sari (Suara Utama - Lembut & Natural)":     {"pitch": 1.15, "rate": 0.98},
    "👩 Dian (Eksekutif - Formal & Profesional)":   {"pitch": 1.05, "rate": 1.02},
    "👩 Nadia (Customer Service - Ramah & Cepat)":  {"pitch": 1.25, "rate": 1.12},
    "👩 Amalia (Presenter - Jelas & Berirama)":     {"pitch": 1.10, "rate": 1.00},
    "👩 Citra (Gaya Santai - Akrab & Logat Kota)":  {"pitch": 1.20, "rate": 1.05},
    "👨 Budi (Suara Utama - Berat & Karismatik)":   {"pitch": 0.72, "rate": 0.92},
    "👨 Andika (Narator - Tegas & Berwibawa)":       {"pitch": 0.65, "rate": 0.98},
    "👨 Rendi (Teknisi Toko - Cepat & Energetik)":   {"pitch": 0.88, "rate": 1.15},
    "👨 Gunawan (Manajer - Tenang & Bijaksana)":     {"pitch": 0.78, "rate": 0.90},
    "👨 Fajar (Gaya Santai - Casual & Friendly)":    {"pitch": 0.85, "rate": 1.02}
}

# 3. Penggabungan Aturan SQL Ketat & Instruksi Tambahan Emotikon 📝
sql_character_instruction = """
You are a smart and professional AI assistant specializing in querying a computer store's SQL database to answer user questions.
You have access to tools for inspecting the database schema and executing SQL queries.

[EMOJI RULE]
- ALWAYS add highly relevant and vibrant emojis to sentences or words when explaining interesting facts, numbers, or data findings to make it super engaging!

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
- If the SQL query returns no rows, politely inform the user that no
