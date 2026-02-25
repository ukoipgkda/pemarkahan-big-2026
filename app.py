import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sistem BIG v5.0", layout="centered")

# --- 1. MUAT DATA ---
@st.cache_data
def load_data():
    try:
        # Kita baca fail CSV anda
        df = pd.read_csv('data.csv', dtype=str)
        # Kita bersihkan No_KP supaya hanya tinggal nombor bulat
        df['No_KP'] = df['No_KP'].str.split('.').str[0].str.strip()
        return df
    except Exception as e:
        st.error(f"Gagal membaca fail: {e}")
        return pd.DataFrame()

# Simpan data dalam session supaya tidak hilang bila refresh
if 'database' not in st.session_state:
    df = load_data()
    if not df.empty:
        # Tambah kolum tambahan yang diperlukan
        cols = ['Siri_BIG', 'Kumpulan', 'No_Dalam_Kumpulan', 'Alahan', 'Ubat', 'No_Kecemasan', 'HP3', 'HP8_I', 'HP8_K', 'Nota']
        for c in cols:
            if c not in df.columns:
                df[c] = ""
        # Set markah permulaan 70
        df[['HP3', 'HP8_I', 'HP8_K']] = [25.0, 15.0, 30.0]
        st.session_state.database = df

# --- NAVIGASI ---
st.sidebar.title("MENU")
mod = st.sidebar.radio("Pilih:", ["Halaman Utama", "Pelajar", "Pensyarah"])

if mod == "Halaman Utama":
    st.title("🏕️ Sistem BIG")
    st.write("Sila pilih menu di sebelah kiri.")

elif mod == "Pelajar":
    st.header("📝 Mod Pelajar")
    kp_masuk = st.text_input("Masukkan No. IC (Contoh: 60706142030)").strip()
    
    if kp_masuk:
        db = st.session_state.database
        # CARIAN AGRESIF: Kita cari IC yang 'ada' dalam data
        match = db[db['No_KP'] == kp_masuk]
        
        if not match.empty:
            idx = match.index[0]
            st.success(f"Ditemui: {db.at[idx, 'Nama_Pelajar']}")
            
            with st.form("daftar"):
                siri = st.selectbox("Siri BIG", [2,3,4])
                kump = st.selectbox("Kumpulan", ["Grey", "Jingga", "Kuning", "Ungu", "Biru Gelap", "Biru", "Pink", "Coklat", "Merah", "Hijau"])
                no_k = st.number_input("No dlm Kumpulan", 1, 20)
                alah = st.text_input("Alahan", value=str(db.at[idx, 'Alahan']))
                tel = st.text_input("No Tel Waris", value=str(db.at[idx, 'No_Kecemasan']))
                
                if st.form_submit_button("Simpan"):
                    st.session_state.database.at[idx, 'Siri_BIG'] = siri
                    st.session_state.database.at[idx, 'Kumpulan'] = kump
                    st.session_state.database.at[idx, 'No_Dalam_Kumpulan'] = no_k
                    st.session_state.database.at[idx, 'Alahan'] = alah
                    st.session_state.database.at[idx, 'No_Kecemasan'] = tel
                    st.success("Data Disimpan!")
        else:
            st.error("No. IC tidak dijumpai. Sila pastikan anda menaip nombor yang betul.")
            with st.expander("Lihat Senarai IC dalam sistem (Guna untuk test)"):
                st.write(db['No_KP'].head(10).tolist())

elif mod == "Pensyarah":
    st.header("🎯 Mod Pensyarah")
    pw = st.sidebar.text_input("Password", type="password")
    if pw == "BIG2026":
        # Gunakan dropdown untuk carian manual jika kod kumpulan belum diisi pelajar
        n_list = st.session_state.database['Nama_Pelajar'].tolist()
        pilih = st.selectbox("Cari Nama Pelajar", [""] + n_list)
        if pilih:
            idx = st.session_state.database[st.session_state.database['Nama_Pelajar'] == pilih].index[0]
            p = st.session_state.database.loc[idx]
            st.write(f"Markah: {p['Nama_Pelajar']}")
            st.info(f"Kumpulan: {p['Kumpulan']} No: {p['No_Dalam_Kumpulan']}")
            m1 = st.number_input("HP3 (Max 25)", 0.0, 25.0, float(p['HP3']))
            if st.button("Simpan Markah"):
                st.session_state.database.at[idx, 'HP3'] = m1
                st.success("Tersimpan!")
