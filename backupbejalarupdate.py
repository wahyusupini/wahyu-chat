import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime
import time

# 1. Konfigurasi Halaman Utama 🚀
st.set_page_config(page_title="Gemini SQL Chatbot Pro", page_icon="💻", layout="centered")

# ==================== FITUR PREMIUM: CUSTOM CSS BACKGROUND & WARNA JAM JELAS ====================
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
        animation:
