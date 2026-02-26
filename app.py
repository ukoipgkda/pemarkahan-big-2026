import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Sistem BIG Premium", layout="centered")

# CSS untuk UI Indigo
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F8FAFC; }
    .stImage > img { border-radius: 15px; border: 3px solid #6366F1; }
    </style>
""", unsafe_allow_html=True)

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(ttl=2)
    
    # --- FUNGSI PENGECAMAN KOLUM AUTOMATIK ---
    # Kita cari kolum tanpa peduli ejaan besar/kecil atau ruang kosong
    cols = {col.strip().upper(): col for col in df.columns}
    
    # Cari kolum IC
    ic_col = next((v for k, v in cols.items() if "KP" in k or "IC" in k), None)
    # Cari kolum Gambar
    img_col = next((v for k, v in cols.items() if "URL" in k or "GAMBAR" in k), None)
    # Cari kolum Nama
    name_col = next((v for k, v in cols.items() if "NAMA" in k), None)

    if ic_col:
        df[ic_col] = df[ic_col].astype(str).str.split('.').str[0].str.strip()

except Exception as e:
    st.error(f"Gagal menyambung: {e}")
    st.stop()

st.title("🏕️ BIG Live System")

ic_input = st.text_input("Masukkan No. IC (060214020918)").strip()

if ic_input and ic_col:
    match = df[df[ic_col] == ic_input]
    
    if not match.empty:
        idx = match.index[0]
        p = match.iloc[0]
        
        # Paparan Gambar Pelajar
        st.write(f"### Selamat Datang, {p[name_col] if name_col else ''}")
        
        # Logik paparan gambar yang selamat
        display_url = "https://via.placeholder.com/150"
        if img_col and pd.notna(p[img_col]) and str(p[img_col]).startswith('http'):
            display_url = p[img_col]
        
        st.image(display_url, width=150)
        
        with st.form("update"):
            st.info("Kemaskini maklumat di bawah:")
            # Tambahkan field mengikut keperluan anda
            if st.form_submit_button("Simpan Ke Google Sheets"):
                conn.update(data=df)
                st.success("Data disimpan!")
                st.cache_data.clear()
    else:
        st.error("Pelajar tidak ditemui.")
