import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Konfigurasi UI
st.set_page_config(page_title="BIG Premium System", layout="centered")

# CSS untuk UI Slate & Indigo yang Premium
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F8FAFC; }
    .stTabs [aria-selected="true"] { background-color: #6366F1 !important; color: white !important; }
    .profile-img { 
        border-radius: 50%; 
        object-fit: cover; 
        border: 4px solid #6366F1;
        margin-bottom: 20px;
    }
    .card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# Integrasi Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/1yzQzxJcTef2pHaKHSxZroFdmgTxR3BRZrSSl_ntuHMM/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=2)
def load_live_data():
    return conn.read(spreadsheet=SHEET_URL)

df = load_live_data()

st.markdown("<h1 style='text-align: center; color: #1E293B;'>🏕️ BIG Management System</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["👤 Mod Pelajar", "🎓 Mod Pensyarah"])

# --- MOD PELAJAR ---
with tab1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    ic_input = st.text_input("No. Kad Pengenalan untuk Akses")
    
    if ic_input:
        # Bersihkan format IC
        df['No_KP'] = df['No_KP'].astype(str).str.split('.').str[0].str.strip()
        match = df[df['No_KP'] == ic_input.strip()]
        
        if not match.empty:
            idx = match.index[0]
            pelajar = match.iloc[0]

            # --- PAPARAN GAMBAR PELAJAR ---
            col_img, col_info = st.columns([1, 2])
            with col_img:
                if pd.notna(pelajar['Url Gambar']) and str(pelajar['Url Gambar']).startswith('http'):
                    st.image(pelajar['Url Gambar'], width=150, caption="Gambar Profil")
                else:
                    st.image("https://via.placeholder.com/150", width=150, caption="Tiada Gambar")
            
            with col_info:
                st.subheader(pelajar['Nama_Pelajar'])
                st.write(f"ID: {pelajar['ID_SISTEM']} | Kelas: {pelajar['Kelas']}")

            # Form Update
            with st.form("form_update_pelajar"):
                siri = st.selectbox("SIRI BIG", [2, 3, 4], index=0)
                kump = st.selectbox("KUMPULAN BIG", ["Grey", "Jingga", "Kuning", "Ungu", "Biru Gelap", "Biru", "Pink", "Coklat", "Merah", "Hijau"])
                no_k = st.number_input("No Dalam Kumpulan", 1, 30, value=1)
                alah = st.text_input("Alahan", value=str(pelajar['Alahan'] or ""))
                tel = st.text_input("No tel Kecemasan", value=str(pelajar['No tel Kecemasan'] or ""))
                
                if st.form_submit_button("Kemaskini Profil Sekarang"):
                    df.at[idx, 'SIRI BIG'] = siri
                    df.at[idx, 'KUMPULAN BIG'] = kump
                    df.at[idx, 'No Dalam Kumpulan'] = no_k
                    df.at[idx, 'Alahan'] = alah
                    df.at[idx, 'No tel Kecemasan'] = tel
                    
                    conn.update(spreadsheet=SHEET_URL, data=df)
                    st.success("Berjaya! Data anda telah dikemaskini secara Live.")
                    st.cache_data.clear()
        else:
            st.error("No. KP tidak ditemui.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- MOD PENSYARAH (SAMA SEPERTI SEBELUM INI) ---
with tab2:
    # ... Kod Pensyarah yang memaparkan gambar juga ...
    st.info("Log masuk di sidebar untuk akses pensyarah.")
