import streamlit as st
import pandas as pd
import requests
import json

# 1. Konfigurasi UI Premium
st.set_page_config(page_title="BIG Smart System 2026", layout="centered")

# URL Apps Script anda
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzxdLIYX82gbl0jgjFWNuQ7UPpg3hIitImIOr1ZtHRjobgfvTRby0sRyAElNv4Y69yCzw/exec"
# URL CSV untuk paparan data
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1yzQzxJcTef2pHaKHSxZroFdmgTxR3BRZrSSl_ntuHMM/gviz/tq?tqx=out:csv"

# CSS Liquid Glassmorphism & Inter Font
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .stApp {
        background: radial-gradient(circle at top left, #1e1b4b 0%, #0f172a 100%);
        font-family: 'Inter', sans-serif;
        color: #f8fafc;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 24px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }

    .profile-img {
        border-radius: 20px;
        border: 3px solid #6366f1;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
        margin-bottom: 1.5rem;
    }

    .stButton>button {
        background: linear-gradient(90deg, #4f46e5, #818cf8);
        color: white; border: none; border-radius: 12px;
        font-weight: 800; height: 3.5rem; width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(79, 70, 229, 0.4);
    }

    input, select, textarea {
        background-color: rgba(255,255,255,0.05) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=5)
def load_data():
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        df.columns = [str(c).strip() for c in df.columns]
        df['No_KP'] = df['No_KP'].astype(str).str.split('.').str[0].str.strip()
        return df
    except:
        return pd.DataFrame()

df = load_data()

# --- HEADER ---
st.markdown("<h1 style='text-align: center; color: white; font-weight: 800; margin-bottom: 0;'>BIG SYSTEM 2026</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #818cf8; font-weight: 600;'>Character Building Portal</p>", unsafe_allow_html=True)

# --- MOD PELAJAR ---
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
ic_input = st.text_input("Gunakan No. IC untuk akses profil (Cth: 060214020918)").strip()

if ic_input:
    match = df[df['No_KP'] == ic_input]
    
    if not match.empty:
        p = match.iloc[0]
        
        # Paparan Visual Profil
        col_v1, col_v2 = st.columns([1, 2])
        with col_v1:
            img = p['Url Gambar'] if pd.notna(p['Url Gambar']) else "https://via.placeholder.com/150"
            st.markdown(f'<img src="{img}" class="profile-img" width="140">', unsafe_allow_html=True)
        with col_v2:
            st.markdown(f"<h2 style='margin:0;'>{p['Nama_Pelajar']}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#818cf8;'>{p['Kelas']} | {p['ID_SISTEM']}</p>", unsafe_allow_html=True)

        st.markdown("<hr style='opacity:0.1'>", unsafe_allow_html=True)

        # Borang Kemaskini
        with st.form("form_update"):
            st.markdown("##### 📝 Kemaskini Maklumat Amali")
            c1, c2 = st.columns(2)
            with c1:
                kump = st.selectbox("Kumpulan BIG", ["Grey", "Jingga", "Kuning", "Ungu", "Biru Gelap", "Biru", "Pink", "Coklat", "Merah", "Hijau"])
                siri = st.selectbox("Siri BIG", [2, 3, 4])
            with c2:
                no_k = st.number_input("No dlm Kumpulan", 1, 30, value=1)
                tel = st.text_input("No Tel Kecemasan", value=str(p.get('No tel Kecemasan', '')))
            
            alah = st.text_input("Alahan", value=str(p.get('Alahan', '')))
            ubat = st.text_input("Ubat-ubatan", value=str(p.get('Ubat-Ubatan', '')))
            
            if st.form_submit_button("SIMPAN DATA KE CLOUD"):
                payload = {
                    "No_KP": ic_input,
                    "Siri_BIG": siri,
                    "Kumpulan_BIG": kump,
                    "No_Kumpulan": no_k,
                    "Alahan": alah,
                    "Ubat": ubat,
                    "No_Kecemasan": tel
                }
                
                try:
                    response = requests.post(APPS_SCRIPT_URL, data=json.dumps(payload))
                    if response.status_code == 200:
                        st.success("✅ Berjaya! Data anda telah disimpan secara Live di Google Sheets.")
                        st.balloons()
                        st.cache_data.clear()
                    else:
                        st.error("Ralat sambungan ke Cloud. Sila cuba lagi.")
                except Exception as e:
                    st.error(f"Ralat Teknis: {e}")
    else:
        st.error("No. IC tidak dijumpai dalam pangkalan data.")
st.markdown("</div>", unsafe_allow_html=True)

st.sidebar.caption("v14.0 Stable | Apps Script API Enabled")
