import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sistem BIG v6.0", layout="centered")

# 1. LOAD DATA
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data.csv', dtype=str)
        # Bersihkan No_KP: Ambil 12 angka sahaja, buang .0
        df['No_KP'] = df['No_KP'].astype(str).apply(lambda x: x.split('.')[0].strip())
        return df
    except Exception as e:
        st.error(f"Ralat: Fail 'data.csv' tidak dijumpai. Sila pastikan anda rename fail CSV anda di GitHub.")
        return pd.DataFrame()

# Simpan dalam Session State
if 'db' not in st.session_state:
    df = load_data()
    if not df.empty:
        # Tambah kolum markah & profil
        for col in ['Siri_BIG', 'Kumpulan', 'No_Dalam_Kumpulan', 'Alahan', 'Ubat', 'No_Kecemasan', 'HP3', 'HP8_I', 'HP8_K', 'Nota']:
            df[col] = df.get(col, "")
        df[['HP3', 'HP8_I', 'HP8_K']] = [25.0, 15.0, 30.0]
        st.session_state.db = df

# --- INTERFACE ---
st.title("🏕️ Sistem Pemarkahan BIG")
mod = st.sidebar.radio("Menu", ["Mod Pelajar", "Mod Pensyarah", "Semak Data"])

if mod == "Semak Data":
    st.subheader("🔍 Isi Kandungan data.csv")
    if 'db' in st.session_state:
        st.write("Jumlah Pelajar:", len(st.session_state.db))
        st.dataframe(st.session_state.db[['Nama_Pelajar', 'No_KP', 'Kelas']].head(10))
    else:
        st.error("Data kosong.")

elif mod == "Mod Pelajar":
    st.header("📝 Pendaftaran Profil")
    metode = st.radio("Cari guna:", ["No. IC", "Pilih Nama dari Senarai"])
    
    idx = None
    db = st.session_state.db

    if metode == "No. IC":
        ic = st.text_input("Masukkan No. IC (Contoh: 60706142030)").strip()
        if ic:
            match = db[db['No_KP'] == ic]
            if not match.empty:
                idx = match.index[0]
            else:
                st.error("IC tidak dijumpai. Cuba cari guna 'Nama' di atas.")
    else:
        nama_pilih = st.selectbox("Pilih Nama Anda:", [""] + db['Nama_Pelajar'].tolist())
        if nama_pilih:
            idx = db[db['Nama_Pelajar'] == nama_pilih].index[0]

    if idx is not None:
        st.success(f"Rekod Ditemui: {db.at[idx, 'Nama_Pelajar']}")
        with st.form("f1"):
            kump = st.selectbox("Kumpulan:", ["Grey", "Jingga", "Kuning", "Ungu", "Biru Gelap", "Biru", "Pink", "Coklat", "Merah", "Hijau"])
            no_k = st.number_input("No dlm Kumpulan:", 1, 20)
            alah = st.text_input("Alahan:", value=str(db.at[idx, 'Alahan']))
            if st.form_submit_button("Simpan"):
                st.session_state.db.at[idx, 'Kumpulan'] = kump
                st.session_state.db.at[idx, 'No_Dalam_Kumpulan'] = no_k
                st.session_state.db.at[idx, 'Alahan'] = alah
                st.success("Tersimpan!")

elif mod == "Mod Pensyarah":
    st.header("🎯 Pemarkahan")
    pw = st.sidebar.text_input("Password", type="password")
    if pw == "BIG2026":
        nama_markah = st.selectbox("Pilih Pelajar untuk Markah:", [""] + st.session_state.db['Nama_Pelajar'].tolist())
        if nama_markah:
            i = st.session_state.db[st.session_state.db['Nama_Pelajar'] == nama_markah].index[0]
            p = st.session_state.db.loc[i]
            st.write(f"Pelajar: {p['Nama_Pelajar']} ({p['Kumpulan']} {p['No_Dalam_Kumpulan']})")
            m = st.number_input("HP3 (Max 25)", 0.0, 25.0, float(p['HP3']))
            if st.button("Update Markah"):
                st.session_state.db.at[i, 'HP3'] = m
                st.success("Markah Dikemaskini!")
        
        st.divider()
        csv = st.session_state.db.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Hasil Akhir (CSV)", csv, "Markah_BIG.csv", "text/csv")
