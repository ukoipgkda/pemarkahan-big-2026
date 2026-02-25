import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Konfigurasi UI Premium & Mobile Responsive
st.set_page_config(page_title="BIG Smart System", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F8FAFC; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: #F1F5F9; padding: 5px; border-radius: 12px; }
    .stTabs [aria-selected="true"] { background-color: #4F46E5 !important; color: white !important; border-radius: 8px; }

    .card {
        background: white; padding: 1.5rem; border-radius: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border: 1px solid #E2E8F0; margin-bottom: 1rem;
    }
    
    .profile-header { text-align: center; margin-bottom: 1rem; }
    .profile-img { border-radius: 50%; border: 4px solid #6366F1; margin-bottom: 10px; object-fit: cover; }
    </style>
""", unsafe_allow_html=True)

# 2. Hubungan Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/1yzQzxJcTef2pHaKHSxZroFdmgTxR3BRZrSSl_ntuHMM/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=2)
def load_data():
    data = conn.read(spreadsheet=SHEET_URL)
    # Bersihkan No_KP agar tidak ralat format
    data['No_KP'] = data['No_KP'].astype(str).str.split('.').str[0].str.strip()
    return data

df = load_data()

# --- HEADER ---
st.markdown("<h2 style='text-align: center; color: #1E293B;'>🏕️ BIG INTEGRATED SYSTEM</h2>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["👤 PROFIL PELAJAR", "🎓 PEMARKAHAN"])

# --- MOD PELAJAR ---
with tab1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    ic_input = st.text_input("Masukkan No. Kad Pengenalan", placeholder="Contoh: 060214020918").strip()

    if ic_input:
        match = df[df['No_KP'] == ic_input]
        
        if not match.empty:
            idx = match.index[0]
            p = match.iloc[0]

            # Paparan Visual Profil
            st.markdown("<div class='profile-header'>", unsafe_allow_html=True)
            img_url = p['Url Gambar'] if pd.notna(p['Url Gambar']) else "https://via.placeholder.com/150"
            st.image(img_url, width=120)
            st.markdown(f"<h3 style='margin:0;'>{p['Nama_Pelajar']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#64748B;'>{p['Kelas']} | {p['ID_SISTEM']}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            with st.form("update_form"):
                c1, c2 = st.columns(2)
                with c1:
                    kump = st.selectbox("KUMPULAN BIG", ["Grey", "Jingga", "Kuning", "Ungu", "Biru Gelap", "Biru", "Pink", "Coklat", "Merah", "Hijau"])
                    siri = st.selectbox("SIRI BIG", [2, 3, 4])
                with c2:
                    no_k = st.number_input("No Dalam Kumpulan", 1, 30, value=1)
                    tel = st.text_input("No tel Kecemasan", value=str(p['No tel Kecemasan'] or ""))
                
                alah = st.text_input("Alahan", value=str(p['Alahan'] or ""))
                ubat = st.text_input("Ubat-Ubatan", value=str(p['Ubat-Ubatan'] or ""))

                if st.form_submit_button("KEMASKINI DATA LIVE"):
                    df.at[idx, 'KUMPULAN BIG'] = kump
                    df.at[idx, 'SIRI BIG'] = siri
                    df.at[idx, 'No Dalam Kumpulan'] = no_k
                    df.at[idx, 'Alahan'] = alah
                    df.at[idx, 'Ubat-Ubatan'] = ubat
                    df.at[idx, 'No tel Kecemasan'] = tel
                    
                    conn.update(spreadsheet=SHEET_URL, data=df)
                    st.balloons()
                    st.success("Data Berjaya Disimpan ke Google Sheets!")
                    st.cache_data.clear()
        else:
            st.error("No. KP tidak dijumpai dalam pangkalan data.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- MOD PENSYARAH ---
with tab2:
    pwd = st.sidebar.text_input("Kata Laluan Pensyarah", type="password")
    if pwd == "BIG2026":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        search_type = st.radio("Kaedah Carian:", ["Kod Kumpulan (C1, M2...)", "Senarai Nama"])
        
        target_idx = None
        if search_type == "Kod Kumpulan (C1, M2...)":
            kod = st.text_input("Taip Kod (Cth: C3)").upper().strip()
            # Logik carian kod kumpulan yang anda mahukan (C=Coklat, dsb)
            if kod:
                import re
                parts = re.findall(r'([A-Z]+)(\d+)', kod)
                if parts:
                    h, n = parts[0]
                    # Map warna ringkas
                    map_c = {'C':'Coklat','M':'Merah','H':'Hijau','B':'Biru','K':'Kuning','J':'Jingga','U':'Ungu','P':'Pink','G':'Grey','BG':'Biru Gelap'}
                    warna = map_c.get(h)
                    res = df[(df['KUMPULAN BIG'] == warna) & (df['No Dalam Kumpulan'].astype(str) == n)]
                    if not res.empty: target_idx = res.index[0]
        else:
            pilih_nama = st.selectbox("Pilih Nama Pelajar", [""] + df['Nama_Pelajar'].tolist())
            if pilih_nama: target_idx = df[df['Nama_Pelajar'] == pilih_nama].index[0]

        if target_idx is not None:
            data_p = df.loc[target_idx]
            st.markdown(f"**Pemarkahan Amali: {data_p['Nama_Pelajar']}**")
            st.image(data_p['Url Gambar'] if pd.notna(data_p['Url Gambar']) else "https://via.placeholder.com/150", width=100)
            
            # Merit/Demerit Slider
            m_hp3 = st.slider("HP3 (Max 25)", 0.0, 25.0, float(data_p.get('HP3', 25.0) or 25.0))
            if st.button("Sahkan Markah"):
                df.at[target_idx, 'HP3'] = m_hp3
                conn.update(spreadsheet=SHEET_URL, data=df)
                st.success("Markah telah dikemaskini secara Live!")
        st.markdown("</div>", unsafe_allow_html=True)
