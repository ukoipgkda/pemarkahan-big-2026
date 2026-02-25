import streamlit as st
import pandas as pd
import re

# Konfigurasi Halaman Mesra Mobile
st.set_page_config(page_title="Sistem BIG MPU3212", layout="centered")

# --- FUNGSI PEMBERSIHAN DATA ---
def clean_kp(val):
    """Memastikan No KP adalah teks bersih tanpa .0 atau ruang kosong"""
    val = str(val).strip()
    if val.endswith('.0'):
        val = val[:-2]
    return val

# --- 1. MUAT DATA ---
@st.cache_data
def load_data():
    try:
        # Membaca data.csv yang anda muat naik
        df = pd.read_csv('data.csv', dtype={'No_KP': str})
        df['No_KP'] = df['No_KP'].apply(clean_kp)
        return df
    except Exception as e:
        st.error(f"Ralat membaca fail data.csv: {e}")
        return pd.DataFrame()

# --- 2. INITIALIZE DATABASE DALAM SESSION ---
if 'database' not in st.session_state:
    raw_df = load_data()
    if not raw_df.empty:
        st.session_state.database = raw_df.copy()
        
        # Tambah kolum tambahan jika belum wujud dalam CSV
        cols_needed = [
            'Siri_BIG', 'Kumpulan', 'No_Dalam_Kumpulan', 
            'Alahan', 'Ubat', 'No_Kecemasan', 
            'HP3', 'HP8_I', 'HP8_K', 'Nota'
        ]
        for col in cols_needed:
            if col not in st.session_state.database.columns:
                st.session_state.database[col] = ""
        
        # Set Markah Default 70/70 (HP3:25, HP8I:15, HP8K:30)
        st.session_state.database[['HP3', 'HP8_I', 'HP8_K']] = [25.0, 15.0, 30.0]
    else:
        st.session_state.database = pd.DataFrame()

# --- 3. MENU UTAMA (SIDEBAR) ---
st.sidebar.title("Menu Utama")
menu = st.sidebar.selectbox("Pilih Mod:", ["Laman Utama", "Mod Pelajar (Update Profil)", "Mod Pensyarah (Pemarkahan)"])

# --- LAMAN UTAMA ---
if menu == "Laman Utama":
    st.title("🏕️ Sistem Pengurusan BIG MPU3212")
    st.write("Selamat Datang ke Sistem Pemarkahan Amali Perkhemahan.")
    st.info("Pelajar: Sila pilih 'Mod Pelajar' untuk mengisi maklumat kumpulan dan alahan.")
    st.info("Pensyarah: Sila pilih 'Mod Pensyarah' untuk melakukan pemarkahan merit/demerit.")

# --- MOD PELAJAR ---
elif menu == "Mod Pelajar (Update Profil)":
    st.header("📝 Profil Pelajar")
    st.write("Sila masukkan No. KP anda untuk mengemaskini maklumat.")
    
    kp_input = st.text_input("No. Kad Pengenalan (Contoh: 010203040506):").strip()
    
    if kp_input:
        db = st.session_state.database
        # Carian tepat No KP
        match = db[db['No_KP'] == kp_input]
        
        if not match.empty:
            idx = match.index[0]
            st.success(f"✅ Nama: {db.at[idx, 'Nama_Pelajar']}")
            
            with st.form("form_biodata"):
                col1, col2 = st.columns(2)
                with col1:
                    siri = st.selectbox("Siri BIG:", [2, 3, 4])
                    kump = st.selectbox("Warna Kumpulan:", ["Grey", "Jingga", "Kuning", "Ungu", "Biru Gelap", "Biru", "Pink", "Coklat", "Merah", "Hijau"])
                with col2:
                    no_k = st.number_input("No. Dalam Kumpulan:", 1, 30, 1)
                    tel = st.text_input("No. Tel Kecemasan (Waris):", value=str(db.at[idx, 'No_Kecemasan']))
                
                alah = st.text_input("Alahan (Jika tiada, tulis TIADA):", value=str(db.at[idx, 'Alahan']))
                ubat = st.text_input("Ubat yang dibawa:", value=str(db.at[idx, 'Ubat']))
                
                if st.form_submit_button("Simpan Maklumat"):
                    st.session_state.database.at[idx, 'Siri_BIG'] = siri
                    st.session_state.database.at[idx, 'Kumpulan'] = kump
                    st.session_state.database.at[idx, 'No_Dalam_Kumpulan'] = no_k
                    st.session_state.database.at[idx, 'Alahan'] = alah
                    st.session_state.database.at[idx, 'Ubat'] = ubat
                    st.session_state.database.at[idx, 'No_Kecemasan'] = tel
                    st.balloons()
                    st.success("Profil berjaya dikemaskini!")
        else:
            st.error("❌ No. KP tidak ditemui dalam pangkalan data.")

# --- MOD PENSYARAH ---
elif menu == "Mod Pensyarah (Pemarkahan)":
    st.header("🎯 Pemarkahan Amali (Default 70%)")
    pw = st.sidebar.text_input("Kata Laluan Pensyarah:", type="password")
    
    if pw == "BIG2026":
        search_mode = st.radio("Kaedah Carian:", ["Kod Kumpulan (C1, M2, dll)", "Carian Nama Manual"])
        
        target_idx = None
        
        if search_mode == "Kod Kumpulan (C1, M2, dll)":
            kod = st.text_input("Masukkan Kod (Contoh: Coklat No. 3 taip 'C3')").upper().strip()
            
            # Mapping Kod kepada Nama Warna
            map_k = {'G':'Grey', 'J':'Jingga', 'K':'Kuning', 'U':'Ungu', 'BG':'Biru Gelap', 'B':'Biru', 'P':'Pink', 'C':'Coklat', 'M':'Merah', 'H':'Hijau'}
            
            if kod:
                parts = re.findall(r'([A-Z]+)(\d+)', kod)
                if parts:
                    k_huruf, k_no = parts[0]
                    k_nama = map_k.get(k_huruf)
                    res = st.session_state.database[
                        (st.session_state.database['Kumpulan'] == k_nama) & 
                        (st.session_state.database['No_Dalam_Kumpulan'] == int(k_no))
                    ]
                    if not res.empty:
                        target_idx = res.index[0]
                    else:
                        st.warning("Data pelajar dengan kod ini belum didaftarkan oleh pelajar.")
        else:
            n_list = st.session_state.database['Nama_Pelajar'].tolist()
            search_n = st.selectbox("Pilih Nama:", [""] + n_list)
            if search_n:
                target_idx = st.session_state.database[st.session_state.database['Nama_Pelajar'] == search_n].index[0]

        if target_idx is not None:
            p = st.session_state.database.loc[target_idx]
            st.subheader(f"👤 {p['Nama_Pelajar']}")
            
            # Info Keselamatan
            st.error(f"🚨 ALAHAN: {p['Alahan'] or 'TIADA'}")
            st.warning(f"💊 UBAT: {p['Ubat'] or 'TIADA'} | 📞 KECEMASAN: {p['No_Kecemasan']}")
            
            # Section Pemarkahan
            st.write("---")
            st.write("### Pelarasan Markah (Merit/Demerit)")
            col_a, col_b, col_c = st.columns(3)
            
            m_hp3 = col_a.number_input("HP3 (Max 25)", 0.0, 25.0, float(p['HP3']))
            m_hp8i = col_b.number_input("HP8-I (Max 15)", 0.0, 15.0, float(p['HP8_I']))
            m_hp8k = col_c.number_input("HP8-K (Max 30)", 0.0, 30.0, float(p['HP8_K']))
            
            nota = st.text_area("Nota (Sebab Merit/Demerit):", value=str(p['Nota']))
            
            if st.button("Simpan Markah"):
                st.session_state.database.at[target_idx, 'HP3'] = m_hp3
                st.session_state.database.at[target_idx, 'HP8_I'] = m_hp8i
                st.session_state.database.at[target_idx, 'HP8_K'] = m_hp8k
                st.session_state.database.at[target_idx, 'Nota'] = nota
                st.success(f"Markah dikemaskini: {m_hp3 + m_hp8i + m_hp8k}/70")

        # Download Button
        st.sidebar.write("---")
        csv_data = st.session_state.database.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button("📥 Download Excel/CSV Markah", csv_data, "Markah_BIG_Lengkap.csv", "text/csv")
    else:
        st.info("Sila masukkan kata laluan untuk akses pemarkahan.")

# --- FOOTER ---
st.sidebar.write("---")
st.sidebar.caption("Sistem Pemarkahan BIG v2.0")
