import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Konfigurasi Halaman & Tema
st.set_page_config(page_title="BIG Premium v10", layout="centered")

# 2. Liquid Glass & Glassmorphism UI (CSS Injection)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Background Liquid Gradient */
    .stApp {
        background: radial-gradient(circle at top left, #e0e7ff 0%, #ffffff 50%, #f1f5f9 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Glassmorphism Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 2rem;
        border-radius: 24px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
        transition: transform 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
    }

    /* Shadcn UI Style Buttons */
    .stButton>button {
        background: #4f46e5;
        color: white;
        border-radius: 12px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        border: none;
        width: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stButton>button:hover {
        background: #4338ca;
        box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.4);
    }

    /* Input Styling */
    .stTextInput input, .stSelectbox div {
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
    }

    /* Profile Image Animation */
    .avatar {
        border-radius: 24px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        border: 4px solid white;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    </style>
""", unsafe_allow_html=True)

# 3. Data Connection
SHEET_URL = "https://docs.google.com/spreadsheets/d/1yzQzxJcTef2pHaKHSxZroFdmgTxR3BRZrSSl_ntuHMM/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=2)
def fetch_data():
    data = conn.read(spreadsheet=SHEET_URL)
    # Autoclean No_KP
    data['No_KP'] = data['No_KP'].astype(str).str.split('.').str[0].str.strip()
    return data

df = fetch_data()

# --- APP LAYOUT ---
st.markdown("<h4 style='text-align: center; color: #6366f1; font-weight: 700; letter-spacing: 2px;'>M P U 3 2 1 2</h4>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #1e293b; margin-top: -10px;'>Character Building System</h1>", unsafe_allow_html=True)

# Menu Navigation (Modern Pill Style)
menu = st.tabs(["👤 My Profile", "⚖️ Scoring Portal"])

# --- MOD PELAJAR (MY PROFILE) ---
with menu[0]:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    ic_input = st.text_input("Access Identity (No. KP)", placeholder="Enter 12 digits...").strip()
    
    if ic_input:
        match = df[df['No_KP'] == ic_input]
        if not match.empty:
            idx = match.index[0]
            p = match.iloc[0]
            
            # Header Profil Modern
            col1, col2 = st.columns([1, 2])
            with col1:
                img_url = p['Url Gambar'] if pd.notna(p['Url Gambar']) else "https://via.placeholder.com/150"
                st.markdown(f'<img src="{img_url}" class="avatar" width="150">', unsafe_allow_html=True)
            with col2:
                st.markdown(f"<h2 style='margin-bottom:0;'>{p['Nama_Pelajar']}</h2>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #6366f1; font-weight: 600;'>{p['Kelas']} • ID: {p['ID_SISTEM']}</p>", unsafe_allow_html=True)

            st.write("---")
            
            # Borang Kemaskini (Shadcn UI style)
            with st.form("update_profile"):
                st.markdown("##### 🛠️ Kemaskini Butiran Amali")
                c1, c2 = st.columns(2)
                with c1:
                    kump = st.selectbox("Kumpulan", ["Grey", "Jingga", "Kuning", "Ungu", "Biru Gelap", "Biru", "Pink", "Coklat", "Merah", "Hijau"])
                    siri = st.selectbox("Siri BIG", [2, 3, 4])
                with c2:
                    no_k = st.number_input("No Dalam Kumpulan", 1, 30, value=1)
                    tel = st.text_input("No Tel Kecemasan", value=str(p['No tel Kecemasan'] or ""))
                
                alah = st.text_input("Maklumat Alahan", value=str(p['Alahan'] or ""))
                
                if st.form_submit_button("Sahkan & Update Cloud"):
                    df.at[idx, 'KUMPULAN BIG'] = kump
                    df.at[idx, 'SIRI BIG'] = siri
                    df.at[idx, 'No Dalam Kumpulan'] = no_k
                    df.at[idx, 'Alahan'] = alah
                    df.at[idx, 'No tel Kecemasan'] = tel
                    
                    conn.update(spreadsheet=SHEET_URL, data=df)
                    st.toast("Profile Synced to Cloud!", icon='🚀')
                    st.cache_data.clear()
        else:
            st.error("Identity not found. Please verify your IC Number.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- MOD PENSYARAH ---
with menu[1]:
    pw = st.sidebar.text_input("Security Key", type="password")
    if pw == "BIG2026":
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 🎯 Live Scoring Portal")
        
        # Carian Pintar
        search_q = st.text_input("Search Student Name or Group Code (C1, M2...)").strip()
        
        # (Logik carian yang telah kita bina sebelum ini diletakkan di sini)
        st.write("Select a student to begin merit/demerit adjustments.")
        st.markdown("</div>", unsafe_allow_html=True)
