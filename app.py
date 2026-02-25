import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sistem BIG v4.0", layout="centered")

# --- FUNGSI PEMBERSIHAN DATA EKSTREM ---
def clean_data(df):
    # Cari kolum yang mengandungi 'KP' atau 'KAD PENGENALAN' (tak kisah huruf besar/kecil)
    kp_col = [c for c in df.columns if 'KP' in c.upper() or 'KAD' in c.upper()]
    if kp_col:
        df = df.rename(columns={kp_col[0]: 'No_KP'})
    
    # Tukar No_KP jadi string bersih
    df['No_KP'] = df['No_KP'].astype(str).apply(lambda x: x.split('.')[0].strip())
    return df

@st.cache_data
def load_data():
    try:
        # Cuba baca fail data.csv
        df = pd.read_csv('data.csv', dtype=str)
        df = clean_data(df)
        return df
    except Exception as e:
        st.error(f"Gagal membaca data.csv: {e}")
        return pd.DataFrame()

# Initialize Database
if 'database' not in st.session_state:
    st.session_state.database = load_data()
    db = st.session_state.database
    if not db.empty:
        # Tambah kolum jika tiada
        for col in ['Siri_BIG', 'Kumpulan', 'No_Dalam_Kumpulan', 'Alahan', 'Ubat', 'No_Kecemasan', 'HP3', 'HP8_I', 'HP8_K', 'Nota']:
            if col not in db.columns:
                db[col] = ""
        db[['HP3', 'HP8_I', 'HP8_K']] = [25.0, 15.0, 30.0]

# --- MENU ---
menu = st.sidebar.radio("Menu", ["Check System", "Mod Pelajar", "Mod Pensyarah"])

if menu == "Check System":
    st.title("🔍 Diagnostik Sistem")
    if st.session_state.database.empty:
        st.error("Fail data.csv kosong atau tidak dijumpai!")
    else:
        st.success("Fail data.csv berjaya dibaca!")
        st.write("Senarai Kolum yang AI nampak:", list(st.session_state.database.columns))
        st.write("Contoh 5 No. KP dalam sistem:", st.session_state.database['No_KP'].head().tolist())
        st.info("Jika No. KP di atas tidak sama dengan IC pelajar, maksudnya fail CSV anda perlu dibetulkan.")

elif menu == "Mod Pelajar":
    st.header("📝 Mod Pelajar")
    kp_input = st.text_input("Masukkan No. IC (Contoh: 010203040506)").strip()
    
    if kp_input:
        db = st.session_state.database
        # Cuba cari yang mengandungi nombor tersebut
        match = db[db['No_KP'] == kp_input]
        
        if not match.empty:
            idx = match.index[0]
            st.success(f"Jumpa! Nama: {db.at[idx, 'Nama_Pelajar']}")
            # ... (form pendaftaran sama seperti sebelum ini) ...
            with st.form("pendaftaran"):
                siri = st.selectbox("Siri", [2,3,4])
                kump = st.selectbox("Kumpulan", ["Grey", "Jingga", "Kuning", "Ungu", "Biru Gelap", "Biru", "Pink", "Coklat", "Merah", "Hijau"])
                no_k = st.number_input("No dlm Kumpulan", 1, 20)
                alah = st.text_input("Alahan", value=str(db.at[idx, 'Alahan']))
                if st.form_submit_button("Simpan"):
                    st.session_state.database.at[idx, 'Siri_BIG'] = siri
                    st.session_state.database.at[idx, 'Kumpulan'] = kump
                    st.session_state.database.at[idx, 'No_Dalam_Kumpulan'] = no_k
                    st.session_state.database.at[idx, 'Alahan'] = alah
                    st.success("Berjaya Simpan!")
        else:
            st.error(f"IC {kp_input} tiada dalam sistem. Sila semak tab 'Check System'.")

elif menu == "Mod Pensyarah":
    st.title("🎯 Pemarkahan")
    pw = st.sidebar.text_input("Password", type="password")
    if pw == "BIG2026":
        st.write("Gunakan carian manual buat masa ini.")
        n_list = st.session_state.database['Nama_Pelajar'].tolist()
        pilih = st.selectbox("Pilih Pelajar", [""] + n_list)
        if pilih:
            idx = st.session_state.database[st.session_state.database['Nama_Pelajar'] == pilih].index[0]
            st.write(f"Markah untuk: {pilih}")
            m1 = st.number_input("HP3", 0.0, 25.0, 25.0)
            if st.button("Simpan"):
                st.session_state.database.at[idx, 'HP3'] = m1
                st.success("Markah disimpan!")
