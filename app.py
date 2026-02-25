# --- MOD PELAJAR (VERSI PEMBETULAN) ---
if menu == "Mod Pelajar (Kemaskini Profil)":
    st.header("📝 Kemaskini Profil Pelajar")
    st.info("Sila masukkan No. KP tanpa tanda sempang (Contoh: 010203040506)")
    
    kp_input = st.text_input("Masukkan No. Kad Pengenalan anda:").strip()
    
    if kp_input:
        # Kita bersihkan data CSV dan input supaya kedua-duanya jadi 'string' untuk perbandingan tepat
        st.session_state.database['No_KP'] = st.session_state.database['No_KP'].astype(str).str.replace('.0', '', regex=False).str.strip()
        
        # Cari pelajar
        match = st.session_state.database[st.session_state.database['No_KP'] == kp_input]
        
        if not match.empty:
            i = match.index[0]
            st.success(f"✅ Rekod Ditemui: {st.session_state.database.at[i, 'Nama_Pelajar']}")
            
            with st.form("form_pelajar"):
                siri = st.selectbox("Siri BIG:", [2, 3, 4])
                kumpulan = st.selectbox("Warna Kumpulan:", ["Grey", "Jingga", "Kuning", "Ungu", "Biru Gelap", "Biru", "Pink", "Coklat", "Merah", "Hijau"])
                no_kump = st.number_input("No. Dalam Kumpulan:", min_value=1, max_value=30, step=1)
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
                    st.success("Profil anda telah berjaya disimpan!")
        else:
            st.error("❌ No. KP tidak ditemui. Sila pastikan No. KP betul atau hubungi Pensyarah.")
            # Paparkan sedikit bantuan untuk debug (Hanya untuk fasa testing)
            with st.expander("Bantuan Debug (Klik jika No KP betul tapi tetap error)"):
                st.write("Senarai 5 No. KP teratas dalam sistem:")
                st.write(st.session_state.database['No_KP'].head())
