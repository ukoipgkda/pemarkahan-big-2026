import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Konfigurasi UI Premium
st.set_page_config(page_title="BIG Premium v7", layout="centered")

# Styling Premium Slate/Indigo
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F8FAFC; }
    .card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .stButton>button { background-color: #4F46E5; color: white; width: 100%; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# Sambungan Google Sheets
# Pastikan Secrets di Streamlit Cloud diletakkan dengan betul
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Gunakan query SQL ringkas untuk tarik data
    df = conn.read(ttl=2) 
    # Bersihkan No_KP
    df['No_KP'] = df['No_KP'].astype(str).str.split('.').str[0].str.strip()
except Exception as e:
    st.error(f"Sambungan GSheets Gagal: {e}")
    st.info("Sila pastikan 'Secrets' di Streamlit Cloud telah diisi.")
    st.stop()

# --- MENU ---
st.title("🏕️ BIG Live System")
tab1, tab2 = st.tabs(["👤 Pelajar", "🎓 Pensyarah"])

# --- MOD PELAJAR ---
with tab1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    ic_input = st.text_input("Masukkan No. IC (Cth: 060214020918)")
    
    if ic_input:
        match = df[df['No_KP'] == ic_input.strip()]
        if not match.empty:
            idx = match.index[0]
            pelajar = match.iloc[0]
            
            # Papar Gambar jika ada
            if pd.notna(pelajar['Url Gambar']):
                st.image(pelajar['Url Gambar'], width=120)
            
            st.success(f"Nama: {pelajar['Nama_Pelajar']}")
            
            with st.form("pendaftaran_live"):
                kump = st.selectbox("KUMPULAN BIG", ["Grey", "Jingga", "Kuning", "Ungu", "Biru Gelap", "Biru", "Pink", "Coklat", "Merah", "Hijau"])
                no_k = st.number_input("No dlm Kumpulan", 1, 30, value=1)
                alah = st.text_input("Alahan", value=str(pelajar['Alahan'] or ""))
                
                if st.form_submit_button("Simpan Data ke Cloud"):
                    # Update Dataframe
                    df.at[idx, 'KUMPULAN BIG'] = kump
                    df.at[idx, 'No Dalam Kumpulan'] = no_k
                    df.at[idx, 'Alahan'] = alah
                    
                    # TOLAK DATA KE GOOGLE SHEETS
                    conn.update(data=df)
                    st.success("✅ Data Berjaya Disimpan di Google Sheets!")
                    st.cache_data.clear()
        else:
            st.error("IC tidak dijumpai.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- MOD PENSYARAH ---
with tab2:
    if st.sidebar.text_input("Password", type="password") == "BIG2026":
        st.subheader("Pemarkahan Live")
        nama_sel = st.selectbox("Pilih Pelajar", [""] + df['Nama_Pelajar'].tolist())
        if nama_sel:
            p_idx = df[df['Nama_Pelajar'] == nama_sel].index[0]
            curr_p = df.iloc[p_idx]
            
            new_hp3 = st.number_input("HP3 (Max 25)", 0.0, 25.0, float(curr_p['HP3'] or 25.0))
            if st.button("Sahkan Markah"):
                df.at[p_idx, 'HP3'] = new_hp3
                conn.update(data=df)
                st.success("Markah Dikemaskini!")
                st.cache_data.clear()

# --- DEBUG TAB (HANYA UNTUK ANDA) ---
with st.sidebar.expander("🛠️ Debug Data"):
    st.write("Senarai Kolum:", df.columns.tolist())
    st.write("Data Mentah (3 baris):", df.head(3))
