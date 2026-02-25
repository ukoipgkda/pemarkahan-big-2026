import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Konfigurasi UI & Tema Premium
st.set_page_config(page_title="BIG Smart System", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #F8FAFC;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #F1F5F9;
        padding: 5px;
        border-radius: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        color: #64748B;
    }

    .stTabs [aria-selected="true"] {
        background-color: #4F46E5 !important;
        color: white !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .profile-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05);
        border: 1px solid #E2E8F0;
        text-align: center;
        margin-bottom: 2rem;
    }

    .profile-img {
        border-radius: 50%;
        border: 4px solid #6366F1;
        object-fit: cover;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Integrasi Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/1yzQzxJcTef2pHaKHSxZroFdmgTxR3BRZrSSl_ntuHMM/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=5)
def load_data():
    df = conn.read(spreadsheet=SHEET_URL)
    # Bersihkan No_KP
    df['No_KP'] = df['No_KP'].astype(str).str.split('.').str[0].str.strip()
    return df

df = load_data()

# --- HEADER ---
st.markdown("<h1 style='text-align: center; color: #1E293B; margin-bottom:0;'>🏕️ BIG INTEGRATED SYSTEM</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6366F1; font-weight:600;'>KURSUS MPU3212/MPU3411</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["👤 MOD PELAJAR", "🎓 MOD PENSYARAH"])

# --- MOD PELAJAR ---
with tab1:
    st.write("### Sila masukkan No. KP untuk kemaskini profil")
    ic_input = st.text_input("No. Kad Pengenalan", placeholder="Contoh: 060214020918").strip()

    if ic_input:
        match = df[df['No_KP'] == ic_input]
        
        if not match.empty:
            idx = match.index[0]
            p = match.iloc[0]

            # PAPARAN KAD PROFIL PREMIUM
            st.markdown("<div class='profile-card'>", unsafe_allow_html=True)
            
            # Tunjukkan gambar pelajar
            url_gambar = p['Url Gambar'] if pd.notna(p['Url Gambar']) else "https://via.placeholder.com/150"
            st.image(url_gambar, width=120)
            
            st.markdown(f"<h2 style='margin:10px 0 5px 0;'>{p['Nama_Pelajar']}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#64748B;'>{p['Kelas']} | {p['No_KP']}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            

            # BORANG KEMASKINI
            with st.form("update_form"):
                c1, c2 = st.columns(2)
                with c1:
                    siri = st.selectbox("SIRI BIG", [2, 3, 4], index=0)
                    kump = st.selectbox("KUMPULAN BIG", ["Grey", "Jingga", "Kuning", "Ungu", "Biru Gelap", "Biru", "Pink", "Coklat", "Merah", "Hijau"])
                with c2:
                    no_k = st.number_input("No Dalam Kumpulan", 1, 30, value=1)
                    tel = st.text_input("No Tel Kecemasan", value=str(p['No tel Kecemasan'] or ""))
                
                alah = st.text_input("Alahan / Masalah Kesihatan", value=str(p['Alahan'] or ""))
                ubat = st.text_input("Ubat-Ubatan", value=str(p['Ubat-Ubatan'] or ""))

                if st.form_submit_button("KEMASKINI PROFIL"):
                    df.at[idx, 'SIRI BIG'] = siri
                    df.at[idx, 'KUMPULAN BIG'] = kump
                    df.at[idx, 'No Dalam Kumpulan'] = no_k
                    df.at[idx, 'Alahan'] = alah
                    df.at[idx, 'Ubat-Ubatan'] = ubat
                    df.at[idx, 'No tel Kecemasan'] = tel
                    
                    conn.update(spreadsheet=SHEET_URL, data=df)
                    st.balloons()
                    st.success("Data anda telah disimpan ke dalam Google Sheets secara LIVE!")
                    st.cache_data.clear()
        else:
            st.error("Ralat: No. KP tidak dijumpai dalam sistem.")

# --- MOD PENSYARAH ---
with tab2:
    st.sidebar.markdown("### Kawalan Pensyarah")
    pwd = st.sidebar.text_input("Kata Laluan", type="password")
    
    if pwd == "BIG2026":
        st.subheader("Carian & Pemarkahan")
        kod = st.text_input("Imbas/Taip Kod Kumpulan (Cth: C3)").upper()
        
        # Logik carian kod kumpulan yang sama...
        # Paparkan gambar pelajar juga di sini supaya pensyarah kenal pelajar tersebut
        st.info("Pilih pelajar untuk mula memberikan markah Merit/Demerit.")
    else:
        st.warning("Sila masukkan kata laluan di bar sisi.")
