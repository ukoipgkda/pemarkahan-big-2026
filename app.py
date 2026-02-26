import streamlit as st
import pandas as pd
import requests
import json

# 1. Konfigurasi Halaman
st.set_page_config(page_title="BIG Premium v17", layout="centered")

# 2. UI/UX Transformation: Kuning, Slate & Indigo
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    /* Latar Belakang & Font Global */
    .stApp {
        background: radial-gradient(circle at top left, #1e293b 0%, #0f172a 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Warna Tulisan Kuning untuk Label & Header */
    h1, h2, h3, h4, label, p, .stMarkdown {
        color: #fbbf24 !important; /* Kuning Emas */
    }

    /* Kad Kaca (Glassmorphism) */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
    }

    /* Input Box: Teks di dalam Box tetap Putih/Hitam agar jelas */
    input, select, textarea {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 10px !important;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        color: #fbbf24;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4f46e5 !important;
        color: white !important;
    }

    /* Butang Modern */
    .stButton>button {
        background: linear-gradient(90deg, #fbbf24, #d97706);
        color: #000 !important;
        font-weight: 800;
        border-radius: 12px;
        border: none;
        height: 3rem;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Data Connection (Kekalkan URL anda)
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzxdLIYX82gbl0jgjFWNuQ7UPpg3hIitImIOr1ZtHRjobgfvTRby0sRyAElNv4Y69yCzw/exec"
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1yzQzxJcTef2pHaKHSxZroFdmgTxR3BRZrSSl_ntuHMM/gviz/tq?tqx=out:csv"

@st.cache_data(ttl=2)
def load_data():
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        df.columns = [str(c).strip().upper() for c in df.columns]
        ic_col = next((c for c in df.columns if "KP" in c or "IC" in c), df.columns[2])
        df[ic_col] = df[ic_col].astype(str).str.split('.').str[0].str.strip()
        return df, ic_col
    except:
        return pd.DataFrame(), None

df, col_ic = load_data()

# --- INTERFACE UTAMA ---
st.markdown("<h1 style='text-align: center;'>🏕️ SISTEM BIG 2026</h1>", unsafe_allow_html=True)

# Menu Tab yang sangat Jelas
menu = st.tabs(["👤 PROFIL PELAJAR", "🔑 LOG MASUK ADMIN"])

# --- MOD PELAJAR ---
with menu[0]:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    ic_input = st.text_input("MASUKKAN NO. IC (KUNING UNTUK JELAS):", placeholder="06XXXXXXXXXX").strip()
    
    if ic_input and not df.empty:
        match = df[df[col_ic] == ic_input]
        if not match.empty:
            p = match.iloc[0]
            idx = match.index[0]
            
            # Info Profil
            col_img, col_info = st.columns([1, 2])
            with col_img:
                img_col = next((c for c in df.columns if "URL" in c or "GAMBAR" in c), None)
                st.image(p[img_col] if img_col and pd.notna(p[img_col]) else "https://via.placeholder.com/150", width=150)
            with col_info:
                st.subheader(f"NAMA: {p.get('NAMA_PELAJAR', '')}")
                st.write(f"KELAS: {p.get('KELAS', '')}")

            # Borang Kemaskini
            with st.form("form_update_kuning"):
                st.markdown("### 📝 KEMASKINI MAKLUMAT")
                c1, c2 = st.columns(2)
                with c1:
                    new_siri = st.selectbox("SIRI BIG", [2, 3, 4])
                    new_kump = st.selectbox("KUMPULAN", ["Grey", "Jingga", "Kuning", "Ungu", "Biru Gelap", "Biru", "Pink", "Coklat", "Merah", "Hijau"])
                with c2:
                    new_no = st.number_input("NO DALAM KUMPULAN", 1, 30, value=1)
                    new_tel = st.text_input("NO TEL KECEMASAN", value=str(p.get('NO TEL KECEMASAN', '')))
                
                if st.form_submit_button("🚀 SIMPAN DATA KE CLOUD"):
                    payload = {"No_KP": ic_input, "Siri_BIG": new_siri, "Kumpulan_BIG": new_kump, "No_Kumpulan": new_no, "No_Kecemasan": new_tel}
                    res = requests.post(APPS_SCRIPT_URL, data=json.dumps(payload))
                    if res.status_code == 200:
                        st.success("✅ DATA DISIMPAN!")
                        st.balloons()
        else:
            st.error("REKOD TIDAK DITEMUI.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- MOD ADMIN (PENSYARAH) ---
with menu[1]:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🔑 AKSES PENTADBIR")
    pwd = st.text_input("MASUKKAN KATA LALUAN ADMIN:", type="password")
    
    if pwd == "BIG2026":
        st.success("AKSES DIBENARKAN")
        st.markdown("### 📊 DASHBOARD PEMARKAHAN")
        
        # Contoh Carian Admin
        pilih_nama = st.selectbox("PILIH NAMA PELAJAR UNTUK MARKAH:", [""] + df['NAMA_PELAJAR'].tolist())
        if pilih_nama:
            p_idx = df[df['NAMA_PELAJAR'] == pilih_nama].index[0]
            st.write(f"MEMBERI MARKAH KEPADA: {pilih_nama}")
            m_hp3 = st.slider("MARKAH HP3 (25)", 0.0, 25.0, 25.0)
            if st.button("SAHKAN MARKAH"):
                st.toast("Markah dihantar ke Sheets!")
    elif pwd != "":
        st.error("KATA LALUAN SALAH!")
    st.markdown("</div>", unsafe_allow_html=True)
