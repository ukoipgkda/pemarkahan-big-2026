import streamlit as st
import pandas as pd

# Konfigurasi Halaman Mesra Mobile
st.set_page_config(page_title="Sistem Pemarkahan BIG", layout="centered")

# 1. LOAD DATA
@st.cache_data
def load_data():
    # Mengambil data dari fail yang anda muat naik
    df = pd.read_csv('SENARAI NAMA MPU3411 2026 - Sheet1.csv')
    return df

df = load_data()

# 2. SESSION STATE (Untuk simpan markah sementara)
if 'database' not in st.session_state:
    # Set markah default 70 untuk semua pelajar
    st.session_state.database = df.copy()
    st.session_state.database['HP3'] = 25.0
    st.session_state.database['HP8_I'] = 15.0
    st.session_state.database['HP8_K'] = 30.0
    st.session_state.database['Nota'] = ""

# 3. ANTARA MUKA (UI)
st.title("🏕️ Sistem Pemarkahan Amali BIG")
st.write("Kursus: MPU3212/MPU3411")

# Login Pensyarah Ringkas
password = st.sidebar.text_input("Kata Laluan Pensyarah", type="password")

if password == "BIG2026": # Anda boleh tukar kata laluan di sini
    st.sidebar.success("Log Masuk Berjaya")
    
    mode = st.radio("Kaedah Carian:", ["Imbas Gambar Tag", "Carian Manual"])
    
    selected_student = None

    if mode == "Imbas Gambar Tag":
        img_file = st.file_uploader("Tangkap Gambar Tag Pelajar", type=['png', 'jpg', 'jpeg'])
        if img_file:
            st.info("Fungsi OCR (Membaca teks dari gambar) sedang memproses... (Simulasi)")
            # Nota: Untuk OCR sebenar, kita perlukan library pytesseract/easyocr
            # Sebagai fallback, kita minta input kod
            tag_code = st.text_input("Sila sahkan Kod Tag (Contoh: C3)")
            if tag_code:
                # Simulasi carian berdasarkan kod kumpulan (Anda perlu tambah kolum Kod dalam CSV jika mahu automatik sepenuhnya)
                st.warning("Pastikan kod kumpulan sepadan dengan senarai.")
    
    else:
        # Carian Manual mesra mobile
        nama_list = df['Nama_Pelajar'].tolist()
        search_name = st.selectbox("Pilih Nama Pelajar / No. KP", [""] + nama_list)
        if search_name:
            selected_student = st.session_state.database[st.session_state.database['Nama_Pelajar'] == search_name].iloc[0]

    # 4. SISTEM PEMARKAHAN (MERIT / DEMERIT)
    if selected_student is not None:
        st.divider()
        st.subheader(f"👤 Profil: {selected_student['Nama_Pelajar']}")
        st.write(f"**Kelas:** {selected_student['Kelas']} | **KP:** {selected_student['No_KP']}")
        
        # Paparan Amaran Alahan (Jika ada dalam data)
        st.error("🚨 ALAHAN: (Sila isi di bahagian profil pelajar)")

        col1, col2, col3 = st.columns(3)
        
        # Nilai Semasa
        idx = st.session_state.database[st.session_state.database['Nama_Pelajar'] == search_name].index[0]
        
        hp3 = col1.number_input("HP3 (Max 25)", 0.0, 25.0, float(selected_student['HP3']))
        hp8i = col2.number_input("HP8-Ind (Max 15)", 0.0, 15.0, float(selected_student['HP8_I']))
        hp8k = col3.number_input("HP8-Kum (Max 30)", 0.0, 30.0, float(selected_student['HP8_K']))
        
        nota = st.text_area("Nota Merit/Demerit (Contoh: -2 Lewat perhimpunan)", selected_student['Nota'])

        if st.button("Simpan Kemaskini Markah"):
            st.session_state.database.at[idx, 'HP3'] = hp3
            st.session_state.database.at[idx, 'HP8_I'] = hp8i
            st.session_state.database.at[idx, 'HP8_K'] = hp8k
            st.session_state.database.at[idx, 'Nota'] = nota
            st.success(f"Markah {selected_student['Nama_Pelajar']} dikemaskini!")
            
            total = hp3 + hp8i + hp8k
            st.metric("Jumlah Markah Semasa", f"{total}/70")

    # 5. EXPORT DATA
    st.divider()
    if st.button("Muat Turun Laporan Markah (CSV)"):
        csv = st.session_state.database.to_csv(index=False).encode('utf-8')
        st.download_button("Klik untuk Download", csv, "Markah_BIG_Terkini.csv", "text/csv")

else:
    st.info("Sila masukkan kata laluan pensyarah di bar sisi untuk memulakan pemarkahan.")
