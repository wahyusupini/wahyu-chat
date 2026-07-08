import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime
import time

# 1. Konfigurasi Halaman Utama
st.set_page_config(page_title="Gemini SQL Chatbot Pro", page_icon="💻", layout="centered")

# ==================== FITUR PREMIUM: VIDEO BACKGROUND PEMANDANGAN BERGERAK TRANSPARAN ====================
# Menyisipkan video pemandangan alam bergerak (looping otomatis, tanpa suara, memenuhi layar, transparan)
st.markdown("""
    <div class="video-bg-container">
        <video autoplay loop muted playsinline class="video-bg">
            <source src="https://assets.mixkit.co/videos/preview/mixkit-beautiful-sunset-over-the-sea-and-mountains-42247-large.mp4" type="video/mp4">
        </video>
        <div class="video-overlay"></div>
    </div>
    
    <style>
    /* Mengunci posisi video sebagai background permanen */
    .video-bg-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -2;
        overflow: hidden;
    }
    .video-bg {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    /* Lapisan overlay transparan agar kontras teks tetap tajam */
    .video-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(15, 23, 42, 0.55); /* Warna gelap transparan */
        z-index: -1;
    }

    /* Mengosongkan background asli Streamlit agar tembus pandang ke video */
    .stApp {
        background: transparent !important;
    }
    
    /* Mengubah Desain Sidebar menjadi Efek Kaca (Glassmorphic Premium) */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.4) !important;
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Membuat Balon Obrolan Berwarna Semi-Transparan (Kristal) */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.12) !important;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 15px;
        color: #f8fafc !important; /* Mengubah teks chat menjadi putih cerah agar mudah dibaca */
        animation: chatPopUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    /* Memastikan teks input di bagian bawah tetap terlihat kontras */
    [data-testid="stChatInput"] {
        background-color: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(255, 2
