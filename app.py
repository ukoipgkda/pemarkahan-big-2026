import streamlit as st
import pandas as pd
import requests
import json

# 1. Konfigurasi Halaman Modern
st.set_page_config(page_title="BIG Premium v15", layout="centered")

# URL Apps Script & CSV (Kekalkan yang anda sudah ada)
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzxdLIYX82gbl0jgjFWNuQ7UPpg3hIitImIOr1ZtHRjobgfvTRby0sRyAElNv4Y69yCzw/exec"
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1yzQzxJcTef2pHaKHSxZroFdmgTxR3BRZrSSl_ntuHMM/gviz/tq?tqx=out:csv"

# 2. Inject Premium CSS (Tailwind & Glassmorphism Vibes)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    /* Latar Belakang Liquid Slate */
    .stApp {
        background: radial-gradient(circle at 0% 0%, #1e293b 0%, #0f172a 100%);
        font-family: 'Inter', sans-serif;
        color: #f1f5f9;
    }

    /* Kad Kaca (Glassmorphism) */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 30px;
        padding: 2.5rem;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        margin-bottom: 2rem;
    }

    /* Animasi Terapung untuk Gambar */
    .avatar-frame {
        border-radius: 25px;
        border: 4px solid #6366f1;
        box-shadow: 0 0 30px rgba(99, 102, 241, 0.4);
        animation: floating 3s ease-in-out infinite;
    }
    @keyframes floating {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-12px); }
    }

    /* Button Indigo Modern */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white; border: none; border-radius: 15px;
        height: 3.8rem; font-weight: 800; font-size: 1.1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%; letter-spacing: 1px;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 15px 30px rgba(79, 70, 229, 0.4);
    }

    /* Input Styling */
    .stTextInput input, .stSelectbox div, .stNumberInput input {
        background-color: rgba(255,255,255,0.07) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 15px !important;
        height: 3rem !important;
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

# --- HEADER SECTION ---
st.markdown("<h4 style='text-align: center; color: #818cf8; letter-spacing: 4px; font-weight: 300;'>INTEGRATED SYSTEM</h4>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-weight: 800; font-size: 3rem; margin-top: -10px;'>BIG 2026</h1>", unsafe_allow_html=True)

# Navigation Menu
menu = st.tabs(["⚡ My Dashboard", "📊 Analytics"])

with menu[0]:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    ic_input = st.text_input("🔑 Masukkan No. IC anda untuk akses:", placeholder="Cth: 060505070453").strip()

    if ic_input:
        match = df[df['No_KP'] == ic_input]
        if not match.empty:
            p = match.iloc[0]
            
            # Profil Visual Modern
            col_v1, col_v2 = st.columns([1, 2])
            with col_v1:
                img_url = p['Url Gambar'] if pd.notna(p['Url Gambar']) else "https://via.placeholder.com/150"
                st.markdown(f'<img src="{img_url}" class="avatar-frame" width="160">', unsafe_allow_html=True)
            
            with col_v2:
                st.markdown(f"<h2 style='margin-bottom:0;'>{p['Nama_Pelajar']}</h2>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #818cf8; font-size: 1.2rem;'>{p['Kelas']} • {p['ID_SISTEM']}</p>", unsafe_allow_html=True)
                st.markdown("<span style='background:#10b981; color:white; padding:4px 12px; border-radius:20px; font-size:0.8rem;'>● Verified Student</span>", unsafe_allow_html=True)

            st.write("---")
            
            # Form Kemaskini Modern dengan Ikon
            with st.form("modern_form"):
                st.markdown("##### 📝 KEMASKINI MAKLUMAT AMALI")
                c1, c2 = st.columns(2)
                with c1:
                    siri = st.selectbox("⛺ Siri BIG", [2, 3, 4], index=([2,3,4].index(int(p['Siri_BIG'])) if pd.notna(p['Siri_BIG']) else 0))
                    kump = st.selectbox("🎨 Kumpulan BIG", ["Grey", "Jingga", "Kuning", "Ungu", "Biru Gelap", "Biru", "Pink", "Coklat", "Merah", "Hijau"])
                with c2:
                    no_k = st.number_input("🔢 No Dalam Kumpulan", 1, 30, value=int(p['No_Kumpulan']) if pd.notna(p['No_Kumpulan']) else 1)
                    tel = st.text_input("📞 No Tel Kecemasan", value=str(p.get('No tel Kecemasan', '')))
                
                alah = st.text_input("⚠️ Alahan (Jika tiada tulis 'Tiada')", value=str(p.get('Alahan', '')))
                ubat = st.text_input("💊 Ubat-ubatan", value=str(p.get('Ubat-Ubatan', '')))
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.form_submit_button("🚀 SIMPAN KE CLOUD"):
                    payload = {
                        "No_KP": ic_input,
                        "Siri_BIG": siri,
                        "Kumpulan_BIG": kump,
                        "No_Kumpulan": no_k,
                        "Alahan": alah,
                        "Ubat": ubat,
                        "No_Kecemasan": tel
                    }
                    
                    response = requests.post(APPS_SCRIPT_URL, data=json.dumps(payload))
                    if response.status_code == 200:
                        st.toast("Data berjaya dihantar ke Google Sheets!", icon="✅")
                        st.success("✅ Success! Maklumat anda telah dikemaskini secara Live.")
                        st.balloons()
                        st.cache_data.clear()
                    else:
                        st.error("Ralat sambungan. Sila cuba lagi.")
        else:
            st.error("Rekod No. IC tidak dijumpai.")
    st.markdown("</div>", unsafe_allow_html=True)

with menu[1]:
    st.markdown("<div class='glass-card' style='text-align:center;'>", unsafe_allow_html=True)
    st.markdown("### 📈 Ringkasan Pendaftaran")
    st.write("Modul statistik akan muncul di sini secara automatik.")
    st.markdown("</div>", unsafe_allow_html=True)
