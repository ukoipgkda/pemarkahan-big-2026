import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Setting Layout
st.set_page_config(page_title="Sistem BIG v12", layout="centered")

# CSS Ringkas untuk nampak kemas
st.markdown("""
    <style>
    .stButton>button { background-color: #4f46e5; color: white; border-radius: 10px; width: 100%; }
    .stTextInput input { border-radius: 10px; }
    .profile-box { border: 1px solid #e2e8f0; padding: 20px; border-radius: 15px; background-color: white; }
    </style>
""", unsafe_allow_html=True)

# 2. Sambungan Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/1yzQzxJcTef2pHaKHSxZroFdmgTxR3BRZrSSl_ntuHMM/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=2)
def load_data():
    # Membaca data tanpa menghiraukan nama kolum asal (Hanya ambil data mentah)
    df = conn.read(spreadsheet=SHEET_URL)
    # Bersihkan Nama Kolum (Buang space depan/belakang dan tukar ke Huruf Besar)
    df.columns = [str(c).strip().upper() for c in df.columns]
    # Bersihkan No_KP
    df['NO_KP'] = df['NO_KP'].astype(str).str.split('.').str[0].str.strip()
    return df

try:
    df = load_data()
except Exception as e:
    st.error("Gagal menyambung ke Google Sheets. Sila semak Secrets.")
    st.stop()

st.title("🏕️ Sistem Pengurusan BIG")

# --- MOD PELAJAR ---
ic_input = st.text_input("Sila masukkan No. Kad Pengenalan anda (12 angka):", placeholder="Contoh: 060505070453").strip()

if ic_input:
    # Cari pelajar
    match = df[df['NO_KP'] == ic_input]
    
    if not match.empty:
        idx = match.index[0]
        p = match.iloc[0]
        
        st.success(f"Rekod Ditemui: {p['NAMA_PELAJAR']}")
        
        # Paparan Gambar dan Butiran
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Cari kolum gambar secara automatik (mencari perkataan 'URL' atau 'GAMBAR')
            img_col = next((c for c in df.columns if "URL" in c or "GAMBAR" in c), None)
            url_img = p[img_col] if img_col and pd.notna(p[img_col]) else "https://via.placeholder.com/150"
            st.image(url_img, width=150, caption="Gambar Profil")
            
        with col2:
            st.write(f"**Nama:** {p['NAMA_PELAJAR']}")
            st.write(f"**ID:** {p.get('ID_SISTEM', 'N/A')}")
            st.write(f"**Kelas:** {p.get('KELAS', 'N/A')}")

        st.markdown("---")
        st.subheader("📝 Kemaskini Maklumat Amali")
        
        # BORANG KEMASKINI (Pastikan ada Submit Button)
        with st.form("update_profil_big"):
            c1, c2 = st.columns(2)
            
            with c1:
                # Ambil nilai sedia ada dari sheet jika ada
                val_siri = p.get('SIRI BIG', '2')
                new_siri = st.selectbox("Siri BIG", [2, 3, 4], index=[2,3,4].index(int(val_siri)) if str(val_siri).isdigit() else 0)
                
                new_kump = st.selectbox("Kumpulan BIG", ["Grey", "Jingga", "Kuning", "Ungu", "Biru Gelap", "Biru", "Pink", "Coklat", "Merah", "Hijau"])
            
            with c2:
                val_no = p.get('NO DALAM KUMPULAN', '1')
                new_no = st.number_input("No Dalam Kumpulan", 1, 30, value=int(val_no) if str(val_no).isdigit() else 1)
                
                new_tel = st.text_input("No Tel Kecemasan", value=str(p.get('NO TEL KECEMASAN', '')))
            
            new_alah = st.text_input("Alahan (Jika tiada tulis 'Tiada')", value=str(p.get('ALAHAN', '')))
            new_ubat = st.text_input("Ubat-Ubatan", value=str(p.get('UBAT-UBATAN', '')))
            
            # BUTANG SIMPAN
            submit = st.form_submit_button("Simpan Ke Google Sheets")
            
            if submit:
                # Update DataFrame tempatan
                df.at[idx, 'SIRI BIG'] = new_siri
                df.at[idx, 'KUMPULAN BIG'] = new_kump
                df.at[idx, 'NO DALAM KUMPULAN'] = new_no
                df.at[idx, 'ALAHAN'] = new_alah
                df.at[idx, 'UBAT-UBATAN'] = new_ubat
                df.at[idx, 'NO TEL KECEMASAN'] = new_tel
                
                # Push ke Google Sheets
                try:
                    conn.update(spreadsheet=SHEET_URL, data=df)
                    st.success("✅ BERJAYA! Maklumat anda telah dikemaskini dalam Google Sheets.")
                    st.cache_data.clear()
                except Exception as e:
                    st.error(f"Gagal menyimpan: {e}")
    else:
        st.error("No. KP tidak dijumpai dalam pangkalan data.")

st.sidebar.caption("Sistem BIG v12.0 Stable")
