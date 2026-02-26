import streamlit as st
import pandas as pd
import requests
import json

# 1. Konfigurasi UI Premium
st.set_page_config(page_title="BIG Premium v16", layout="centered")

# URL Apps Script & CSV (Kekalkan yang anda sudah ada)
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzxdLIYX82gbl0jgjFWNuQ7UPpg3hIitImIOr1ZtHRjobgfvTRby0sRyAElNv4Y69yCzw/exec"
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1yzQzxJcTef2pHaKHSxZroFdmgTxR3BRZrSSl_ntuHMM/gviz/tq?tqx=out:csv"

# 2. Inject Ultra-Modern CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    .stApp { background: radial-gradient(circle at 0% 0%, #1e293b 0%, #0f172a 100%); font-family: 'Inter', sans-serif; color: #f1f5f9; }
    .glass-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px; padding: 2.5rem; margin-bottom: 2rem; }
    .avatar-frame { border-radius: 25px; border: 4px solid #6366f1; box-shadow: 0 0 30px rgba(99, 102, 241, 0.4); }
    .stButton>button { background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); color: white; border: none; border-radius: 15px; height: 3.8rem; font-weight: 800; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# 3. Fungsi Pengecaman Kolum Automatik (Selesaikan KeyError)
@st.cache_data(ttl=5)
def load_data():
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        # Bersihkan nama kolum: buang space, tukar ke huruf besar
        df.columns = [str(c).strip().upper() for c in df.columns]
        # Cari kolum IC (No_KP)
        ic_col = next((c for c in df.columns if "KP" in c or "IC" in c), df.columns[2])
        df[ic_col] = df[ic_col].astype(str).str.split('.').str[0].str.strip()
        return df, ic_col
    except Exception as e:
        st.error(f"Gagal memuatkan data: {e}")
        return pd.DataFrame(), None

df, col_ic = load_data()

# --- HEADER ---
st.markdown("<h1 style='text-align: center; font-weight: 800;'>BIG SYSTEM 2026</h1>", unsafe_allow_html=True)

# --- MOD PELAJAR ---
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
ic_input = st.text_input("🔑 Masukkan No. IC anda:", placeholder="Cth: 060505070453").strip()

if ic_input and not df.empty:
    match = df[df[col_ic] == ic_input]
    
    if not match.empty:
        idx = match.index[0]
        p = match.iloc[0]
        
        # Pengecaman Kolum Dinamik
        col_nama = next((c for c in df.columns if "NAMA" in c), df.columns[1])
        col_img = next((c for c in df.columns if "URL" in c or "GAMBAR" in c), df.columns[6])
        col_kelas = next((c for c in df.columns if "KELAS" in c), df.columns[5])

        # Header Profil
        c_v1, c_v2 = st.columns([1, 2])
        with c_v1:
            img_url = p[col_img] if pd.notna(p[col_img]) else "https://via.placeholder.com/150"
            st.markdown(f'<img src="{img_url}" class="avatar-frame" width="160">', unsafe_allow_html=True)
        with c_v2:
            st.markdown(f"<h2>{p[col_nama]}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #818cf8;'>{p[col_kelas]}</p>", unsafe_allow_html=True)

        st.write("---")
        
        # --- FORM KEMASKINI (Fixed Missing Submit Button) ---
        with st.form("modern_update_form"):
            st.markdown("##### 📝 KEMASKINI MAKLUMAT")
            f1, f2 = st.columns(2)
            with f1:
                # Cuba dapatkan nilai asal dari sheet
                orig_siri = str(p.get('SIRI BIG', '2'))
                siri_idx = [2,3,4].index(int(orig_siri)) if orig_siri.isdigit() and int(orig_siri) in [2,3,4] else 0
                new_siri = st.selectbox("⛺ Siri BIG", [2, 3, 4], index=siri_idx)
                
                new_kump = st.selectbox("🎨 Kumpulan BIG", ["Grey", "Jingga", "Kuning", "Ungu", "Biru Gelap", "Biru", "Pink", "Coklat", "Merah", "Hijau"])
            
            with f2:
                orig_no = str(p.get('NO DALAM KUMPULAN', '1'))
                new_no = st.number_input("🔢 No Dalam Kumpulan", 1, 30, value=int(orig_no) if orig_no.isdigit() else 1)
                
                new_tel = st.text_input("📞 No Tel Kecemasan", value=str(p.get('NO TEL KECEMASAN', '')))
            
            new_alah = st.text_input("⚠️ Alahan", value=str(p.get('ALAHAN', '')))
            new_ubat = st.text_input("💊 Ubat-ubatan", value=str(p.get('UBAT-UBATAN', '')))
            
            # INI ADALAH BUTANG WAJIB UNTUK FORM
            submitted = st.form_submit_button("🚀 SIMPAN KE GOOGLE SHEETS")
            
            if submitted:
                payload = {
                    "No_KP": ic_input,
                    "Siri_BIG": new_siri,
                    "Kumpulan_BIG": new_kump,
                    "No_Kumpulan": new_no,
                    "Alahan": new_alah,
                    "Ubat": new_ubat,
                    "No_Kecemasan": new_tel
                }
                
                try:
                    response = requests.post(APPS_SCRIPT_URL, data=json.dumps(payload))
                    if response.status_code == 200:
                        st.balloons()
                        st.success("✅ BERJAYA! Maklumat telah dikemaskini secara Live.")
                        st.cache_data.clear()
                    else:
                        st.error("Gagal menyambung ke Cloud. Sila cuba lagi.")
                except Exception as e:
                    st.error(f"Ralat: {e}")
    else:
        st.error("Rekod IC tidak dijumpai.")
st.markdown("</div>", unsafe_allow_html=True)
