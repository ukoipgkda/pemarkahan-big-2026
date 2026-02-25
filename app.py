import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Konfigurasi UI Premium
st.set_page_config(page_title="Sistem BIG Premium", layout="centered")

# CSS untuk gaya Slate/Indigo & Font Inter
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F8FAFC; }
    .main { background-color: #F8FAFC; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #F1F5F9; border-radius: 8px 8px 0px 0px; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #6366F1 !important; color: white !important; }
    div[data-testid="stForm"] { border: none; background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# Integrasi Google Sheets
# ID dari URL anda: 1yzQzxJcTef2pHaKHSxZroFdmgTxR3BRZrSSl_ntuHMM
SHEET_URL = "https://docs.google.com/spreadsheets/d/1yzQzxJcTef2pHaKHSxZroFdmgTxR3BRZrSSl_ntuHMM/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=2) # Data refresh setiap 2 saat untuk live update
def load_live_data():
    return conn.read(spreadsheet=SHEET_URL)

df = load_live_data()

st.markdown("<h1 style='text-align: center; color: #1E293B;'>🏕️ BIG Management System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B;'>Urus maklumat dan pemarkahan amali secara real-time</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["👤 Mod Pelajar", "🎓 Mod Pensyarah"])

# --- MOD PELAJAR ---
with tab1:
    st.markdown("### Kemaskini Biodata")
    search_ic = st.text_input("Masukkan No. Kad Pengenalan (Contoh: 60706142030)")
    
    if search_ic:
        # Pembersihan data IC (String comparison)
        df['No_KP'] = df['No_KP'].astype(str).str.split('.').str[0].str.strip()
        match = df[df['No_KP'] == search_ic.strip()]
        
        if not match.empty:
            idx = match.index[0]
            st.success(f"Rekod Ditemui: {match.iloc[0]['Nama_Pelajar']}")
            
            with st.form("form_pelajar"):
                col1, col2 = st.columns(2)
                with col1:
                    siri = st.selectbox("SIRI BIG", [2, 3, 4])
                    kumpulan = st.selectbox("KUMPULAN BIG", ["Grey", "Jingga", "Kuning", "Ungu", "Biru Gelap", "Biru", "Pink", "Coklat", "Merah", "Hijau"])
                with col2:
                    no_kump = st.number_input("No Dalam Kumpulan", 1, 30, value=1)
                    kecemasan = st.text_input("No Tel Kecemasan", value=str(match.iloc[0]['No tel Kecemasan'] or ""))
                
                alahan = st.text_input("Alahan", value=str(match.iloc[0]['Alahan'] or ""))
                ubat = st.text_input("Ubat-Ubatan", value=str(match.iloc[0]['Ubat-Ubatan'] or ""))
                
                if st.form_submit_button("Sahkan & Simpan"):
                    # Update local dataframe
                    df.at[idx, 'SIRI BIG'] = siri
                    df.at[idx, 'KUMPULAN BIG'] = kumpulan
                    df.at[idx, 'No Dalam Kumpulan'] = no_kump
                    df.at[idx, 'Alahan'] = alahan
                    df.at[idx, 'Ubat-Ubatan'] = ubat
                    df.at[idx, 'No tel Kecemasan'] = kecemasan
                    
                    # Update Google Sheets
                    conn.update(spreadsheet=SHEET_URL, data=df)
                    st.balloons()
                    st.success("Data telah dikemaskini dalam Google Sheets secara LIVE!")
                    st.cache_data.clear()
        else:
            st.error("No. KP tidak ditemui. Sila hubungi urus setia.")

# --- MOD PENSYARAH ---
with tab2:
    st.markdown("### Pemarkahan Amali")
    pwd = st.sidebar.text_input("Kata Laluan Akses", type="password")
    
    if pwd == "BIG2026":
        st.sidebar.success("Akses Dibenarkan")
        
        # Carian Berdasarkan Kod Kumpulan (C1, M2, dll)
        short_code = st.text_input("Imbas / Taip Kod Kumpulan (Contoh: C3)").upper()
        
        target_student = None
        if short_code:
            color_map = {'G':'Grey', 'J':'Jingga', 'K':'Kuning', 'U':'Ungu', 'BG':'Biru Gelap', 'B':'Biru', 'P':'Pink', 'C':'Coklat', 'M':'Merah', 'H':'Hijau'}
            import re
            parts = re.findall(r'([A-Z]+)(\d+)', short_code)
            if parts:
                h, n = parts[0]
                warna = color_map.get(h)
                res = df[(df['KUMPULAN BIG'] == warna) & (df['No Dalam Kumpulan'].astype(str) == n)]
                if not res.empty:
                    target_student = res.iloc[0]
                else:
                    st.warning("Kod tidak ditemui dalam data berdaftar.")

        if target_student is not None:
            st.info(f"Pemarkahan untuk: **{target_student['Nama_Pelajar']}**")
            st.error(f"⚠️ Alahan: {target_student['Alahan'] or 'Tiada'}")
            
            with st.form("form_markah"):
                c1, c2, c3 = st.columns(3)
                m_hp3 = c1.number_input("HP3 (25%)", 0.0, 25.0, float(target_student.get('HP3', 25.0) or 25.0))
                m_hp8i = c2.number_input("HP8-I (15%)", 0.0, 15.0, float(target_student.get('HP8_I', 15.0) or 15.0))
                m_hp8k = c3.number_input("HP8-K (30%)", 0.0, 30.0, float(target_student.get('HP8_K', 30.0) or 30.0))
                
                if st.form_submit_button("Simpan Markah"):
                    df.at[target_student.name, 'HP3'] = m_hp3
                    df.at[target_student.name, 'HP8_I'] = m_hp8i
                    df.at[target_student.name, 'HP8_K'] = m_hp8k
                    conn.update(spreadsheet=SHEET_URL, data=df)
                    st.success(f"Markah {target_student['Nama_Pelajar']} dikemaskini!")
                    st.cache_data.clear()
    else:
        st.info("Sila masukkan kata laluan di bar sisi untuk memulakan pemarkahan.")

st.sidebar.write("---")
st.sidebar.caption("Sistem Bersepadu Google Sheets & Streamlit")
