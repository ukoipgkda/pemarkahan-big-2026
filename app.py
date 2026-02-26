import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. UI & Font Premium
st.set_page_config(page_title="BIG Premium System", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #f8fafc; }
    .stTabs [aria-selected="true"] { background-color: #6366f1 !important; color: white !important; }
    .main-card { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

# 2. Fungsi Sambungan GSheets yang Lebih Stabil
def get_data():
    try:
        # Cuba sambung menggunakan Secrets
        conn = st.connection("gsheets", type=GSheetsConnection)
        data = conn.read(ttl=2)
        return data, None
    except Exception as e:
        return None, str(e)

df, error_msg = get_data()

# --- HEADER ---
st.markdown("<h2 style='text-align: center; color: #1e293b;'>🏕️ BIG INTEGRATED SYSTEM</h2>", unsafe_allow_html=True)

# 3. DIAGNOSTIK (Jika Error)
if error_msg:
    st.error("🚨 Gagal menyambung ke Google Sheets!")
    st.info(f"Ralat Teknis: {error_msg}")
    st.warning("Pastikan anda telah memasukkan 'Secrets' di Dashboard Streamlit Cloud.")
    st.stop()

# --- MENU UTAMA ---
tab1, tab2 = st.tabs(["👤 Kemaskini Pelajar", "🎓 Pemarkahan"])

with tab1:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    ic_input = st.text_input("Log Masuk No. Kad Pengenalan (Cth: 060214020918)").strip()
    
    if ic_input:
        # Normalisasi IC (Buang .0 atau ruang kosong)
        df['No_KP'] = df['No_KP'].astype(str).str.split('.').str[0].str.strip()
        match = df[df['No_KP'] == ic_input]
        
        if not match.empty:
            idx = match.index[0]
            p = match.iloc[0]
            
            # Papar Gambar & Nama
            col_a, col_b = st.columns([1, 3])
            with col_a:
                img = p['Url Gambar'] if pd.notna(p['Url Gambar']) else "https://via.placeholder.com/150"
                st.image(img, width=100)
            with col_b:
                st.subheader(p['Nama_Pelajar'])
                st.write(f"ID: {p['ID_SISTEM']} | Kelas: {p['Kelas']}")

            with st.form("form_pelajar"):
                kump = st.selectbox("Kumpulan", ["Grey", "Jingga", "Kuning", "Ungu", "Biru Gelap", "Biru", "Pink", "Coklat", "Merah", "Hijau"])
                no_k = st.number_input("No dlm Kumpulan", 1, 30, value=int(p['No Dalam Kumpulan']) if pd.notna(p['No Dalam Kumpulan']) and p['No Dalam Kumpulan'] != "" else 1)
                alah = st.text_input("Alahan", value=str(p['Alahan'] or ""))
                tel = st.text_input("No Tel Kecemasan", value=str(p['No tel Kecemasan'] or ""))
                
                if st.form_submit_button("Simpan Data Live"):
                    try:
                        # Update dataframe
                        df.at[idx, 'KUMPULAN BIG'] = kump
                        df.at[idx, 'No Dalam Kumpulan'] = no_k
                        df.at[idx, 'Alahan'] = alah
                        df.at[idx, 'No tel Kecemasan'] = tel
                        
                        # Tolak ke GSheets
                        conn = st.connection("gsheets", type=GSheetsConnection)
                        conn.update(data=df)
                        st.balloons()
                        st.success("✅ Berjaya disimpan di Google Sheets!")
                        st.cache_data.clear()
                    except Exception as e:
                        st.error(f"Gagal menulis ke GSheets: {e}")
        else:
            st.error("Pelajar tidak ditemui. Sila semak No. IC.")
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.sidebar.subheader("Akses Pensyarah")
    if st.sidebar.text_input("Password", type="password") == "BIG2026":
        st.write("### Pemarkahan Amali")
        sel_pelajar = st.selectbox("Pilih Pelajar", [""] + df['Nama_Pelajar'].tolist())
        if sel_pelajar:
            p_idx = df[df['Nama_Pelajar'] == sel_pelajar].index[0]
            st.info(f"Memberi markah kepada: {sel_pelajar}")
            # Logik markah ...
    else:
        st.info("Sila masukkan kata laluan untuk pemarkahan.")
