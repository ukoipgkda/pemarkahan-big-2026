import streamlit as st
import pandas as pd
import requests
import json

st.set_page_config(page_title="BIG Smart Scoring", layout="centered")

# --- CSS PREMUM (Kuning & Indigo) ---
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #fbbf24; font-family: 'Inter', sans-serif; }
    .glass-card { background: rgba(255,255,255,0.05); padding: 25px; border-radius: 20px; border: 1px solid #334155; margin-bottom: 20px; }
    h1, h2, h3, label { color: #fbbf24 !important; }
    .stSlider > div > div > div > div { background: #fbbf24; }
    .stButton > button { background: #fbbf24; color: black; font-weight: bold; border-radius: 12px; border: none; width: 100%; height: 3.5rem; }
    </style>
""", unsafe_allow_html=True)

APPS_SCRIPT_URL = "URL_APPS_SCRIPT_ANDA"
CSV_URL = "URL_CSV_GOOGLE_SHEETS_ANDA"

@st.cache_data(ttl=2)
def load_data():
    df = pd.read_csv(CSV_URL)
    df.columns = [str(c).strip().upper() for c in df.columns]
    # Cari kolum IC
    ic_col = next((c for c in df.columns if "KP" in c or "IC" in c), df.columns[2])
    df[ic_col] = df[ic_col].astype(str).str.split('.').str[0].str.strip()
    return df, ic_col

df, col_ic = load_data()

st.title("🏕️ BIG MANAGEMENT SYSTEM 2026")

tabs = st.tabs(["👤 Pendaftaran Profil", "🔑 Dashboard Pemarkahan"])

# --- TAB 1: PENDAFTARAN ---
with tabs[0]:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    ic_user = st.text_input("MASUKKAN NO. IC PELAJAR:", key="ic_user")
    if ic_user:
        match = df[df[col_ic] == ic_user]
        if not match.empty:
            p = match.iloc[0]
            st.success(f"REKOD DITEMUI: {p['NAMA_PELAJAR']}")
            with st.form("update_profil"):
                # (Sila masukkan field biodata seperti siri, kumpulan dsb di sini)
                if st.form_submit_button("SIMPAN DATA PROFIL"):
                    payload = {"type": "profile", "No_KP": ic_user, "Siri_BIG": 2} # Contoh
                    requests.post(APPS_SCRIPT_URL, data=json.dumps(payload))
                    st.toast("Biodata disimpan!")
        else: st.error("IC tidak dijumpai.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 2: PEMARKAHAN (ADMIN) ---
with tabs[1]:
    pwd = st.sidebar.text_input("KATA LALUAN ADMIN:", type="password")
    if pwd == "BIG2026":
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🎯 DASHBOARD PEMARKAHAN LIVE")
        
        # Pilihan Pelajar
        pilih_nama = st.selectbox("PILIH NAMA PELAJAR UNTUK MARKAH:", [""] + df['NAMA_PELAJAR'].tolist())
        
        if pilih_nama:
            target = df[df['NAMA_PELAJAR'] == pilih_nama].iloc[0]
            ic_target = target[col_ic]
            
            st.info(f"Memberi markah kepada: **{pilih_nama}** ({ic_target})")
            
            with st.form("pemarkahan_detail"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**📚 Ujian Teori (10%)**")
                    k1 = st.number_input("Kuiz I (5%)", 0.0, 5.0, 0.0)
                    k2 = st.number_input("Kuiz II (5%)", 0.0, 5.0, 0.0)
                    
                    st.markdown("**⛺ Amali I - Pra (20%)**")
                    h4 = st.number_input("HP4 (10%)", 0.0, 10.0, 0.0)
                    h5 = st.number_input("HP5 (10%)", 0.0, 10.0, 0.0)
                
                with col2:
                    st.markdown("**⛰️ Amali II - Perkhemahan (70%)**")
                    h3 = st.number_input("HP3 (25%)", 0.0, 25.0, 0.0)
                    h8i = st.number_input("HP8 Individu (15%)", 0.0, 15.0, 0.0)
                    h8k = st.number_input("HP8 Kumpulan (30%)", 0.0, 30.0, 0.0)
                
                total = k1 + k2 + h4 + h5 + h3 + h8i + h8k
                st.metric("JUMLAH MARKAH KESELURUHAN", f"{total}%")
                
                if st.form_submit_button("SAHKAN & HANTAR MARKAH"):
                    payload = {
                        "type": "scoring",
                        "No_KP": str(ic_target),
                        "NAMA": pilih_nama,
                        "KUIZ1": k1, "KUIZ2": k2,
                        "HP4": h4, "HP5": h5,
                        "HP3": h3, "HP8I": h8i, "HP8K": h8k
                    }
                    res = requests.post(APPS_SCRIPT_URL, data=json.dumps(payload))
                    if res.status_code == 200:
                        st.balloons()
                        st.success(f"Markah {pilih_nama} berjaya dicatat ke dalam Sheet MARKAH!")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Sila masukkan kata laluan admin di sidebar untuk akses pemarkahan.")
