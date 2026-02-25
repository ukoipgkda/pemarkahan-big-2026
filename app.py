import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sistem BIG MPU3212", layout="centered")

# 1. LOAD DATA
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data.csv')
        return df
    except:
        st.error("Fail data.csv tidak ditemui. Sila pastikan anda telah rename fail CSV anda di GitHub.")
        return pd.DataFrame()

df = load_data()

# Initialize Database dalam Session State
if 'database' not in st.session_state:
    st.session_state.database = df.copy()
    # Tambah kolum baru jika belum wujud
    for col in ['Siri_BIG', 'Kumpulan', 'No_Dalam_Kumpulan', 'Alahan', 'Ubat', 'No_Kecemasan', 'HP3', 'HP8_I', 'HP8_K', 'Nota']:
        if col not in st.session_state.database.columns:
            st.session_state.database[col] = ""
    # Set default markah 70
    st.session_state.database[['HP3', 'HP8_I', 'HP8_K']] = [25.0, 15.0, 30.0]

# --- MENU UTAMA ---
st.title("🏕️ Sistem Pengurusan & Pemarkahan BIG")
menu = st.sidebar.selectbox("Pilih Mod:", ["Laman Utama", "Mod Pelajar (Kemaskini Profil)", "Mod Pensyarah (Pemarkahan)"])

# --- MOD PELAJAR ---
if menu == "Mod Pelajar (Kemaskini Profil)":
    st.header("📝 Kemaskini Profil Pelajar")
    kp_input = st.text_input("Masukkan No. Kad Pengenalan anda:")
    
    if kp_input:
        # Cari pelajar berdasarkan No_KP
        idx = st.session_state.database[st.session_state.database['No_KP'].astype(str).str.contains(kp_input)].index
        
        if not idx.empty:
            i = idx[0]
            st.success(f"Selamat Datang, {st.session_state.database.at[i, 'Nama_Pelajar']}!")
            
            with st.form("form_pelajar"):
                siri = st.selectbox("Siri BIG:", [2, 3, 4])
                kumpulan = st.selectbox("Warna Kumpulan:", ["Grey", "Jingga", "Kuning", "Ungu", "Biru Gelap", "Biru", "Pink", "Coklat", "Merah", "Hijau"])
                no_kump = st.number_input("No. Dalam Kumpulan:", min_value=1, max_value=20, step=1)
                alahan = st.text_input("Alahan (Jika tiada, tulis TIADA):")
                ubat = st.text_input("Ubat-ubatan yang dibawa:")
                kecemasan = st.text_input("No. Telefon Kecemasan (Waris):")
                
                if st.form_submit_button("Simpan Maklumat"):
                    st.session_state.database.at[i, 'Siri_BIG'] = siri
                    st.session_state.database.at[i, 'Kumpulan'] = kumpulan
                    st.session_state.database.at[i, 'No_Dalam_Kumpulan'] = no_kump
                    st.session_state.database.at[i, 'Alahan'] = alahan
                    st.session_state.database.at[i, 'Ubat'] = ubat
                    st.session_state.database.at[i, 'No_Kecemasan'] = kecemasan
                    st.balloons()
                    st.success("Profil anda telah dikemaskini!")
        else:
            st.error("No. KP tidak ditemui dalam senarai rasmi.")

# --- MOD PENSYARAH ---
elif menu == "Mod Pensyarah (Pemarkahan)":
    st.header("🎯 Pemarkahan Amali (Merit/Demerit)")
    pw = st.sidebar.text_input("Kata Laluan:", type="password")
    
    if pw == "BIG2026":
        search_mode = st.radio("Cari Pelajar Melalui:", ["Kod Kumpulan (C3, J1, dll)", "Nama/No.KP"])
        
        target_idx = None
        
        if search_mode == "Kod Kumpulan (C3, J1, dll)":
            kod = st.text_input("Masukkan Kod (Contoh: Coklat 3 tulis 'C3')").upper()
            # Logik ringkas: C=Coklat, J=Jingga, M=Merah, dsb.
            map_kump = {'C':'Coklat', 'J':'Jingga', 'G':'Grey', 'K':'Kuning', 'U':'Ungu', 'BG':'Biru Gelap', 'B':'Biru', 'P':'Pink', 'M':'Merah', 'H':'Hijau'}
            
            if kod:
                # Cuba pecahkan kod, cth 'C3' -> 'C' dan '3'
                import re
                parts = re.findall(r'([A-Z]+)(\d+)', kod)
                if parts:
                    k_huruf, k_no = parts[0]
                    k_nama = map_kump.get(k_huruf)
                    res = st.session_state.database[(st.session_state.database['Kumpulan'] == k_nama) & (st.session_state.database['No_Dalam_Kumpulan'] == int(k_no))]
                    if not res.empty:
                        target_idx = res.index[0]
        
        else:
            search_manual = st.selectbox("Pilih Pelajar:", [""] + st.session_state.database['Nama_Pelajar'].tolist())
            if search_manual:
                target_idx = st.session_state.database[st.session_state.database['Nama_Pelajar'] == search_manual].index[0]

        if target_idx is not None:
            p = st.session_state.database.loc[target_idx]
            st.subheader(f"📍 {p['Nama_Pelajar']}")
            st.warning(f"🚨 ALAHAN: {p['Alahan']} | UBAT: {p['Ubat']}")
            st.info(f"📞 Kecemasan: {p['No_Kecemasan']}")
            
            # Form Markah
            c1, c2, c3 = st.columns(3)
            m_hp3 = c1.number_input("HP3 (25)", 0.0, 25.0, float(p['HP3']))
            m_hp8i = c2.number_input("HP8-I (15)", 0.0, 15.0, float(p['HP8_I']))
            m_hp8k = c3.number_input("HP8-K (30)", 0.0, 30.0, float(p['HP8_K']))
            nota = st.text_area("Nota Merit/Demerit:", p['Nota'])
            
            if st.button("Simpan Markah"):
                st.session_state.database.at[target_idx, 'HP3'] = m_hp3
                st.session_state.database.at[target_idx, 'HP8_I'] = m_hp8i
                st.session_state.database.at[target_idx, 'HP8_K'] = m_hp8k
                st.session_state.database.at[target_idx, 'Nota'] = nota
                st.success("Markah berjaya disimpan!")

        # Download Button
        csv = st.session_state.database.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button("📥 Muat Turun Data Keseluruhan", csv, "Data_BIG_Lengkap.csv", "text/csv")
    else:
        st.info("Sila masukkan kata laluan untuk akses pemarkahan.")

else:
    st.write("Selamat Datang! Pelajar sila pilih **Mod Pelajar** untuk daftar profil. Pensyarah sila pilih **Mod Pensyarah**.")
