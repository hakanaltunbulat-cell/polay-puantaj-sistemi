import streamlit as st
import pandas as pd
from datetime import datetime
import calendar

st.set_page_config(page_title="Polay Puantaj Sistemi", layout="wide", initial_sidebar_state="expanded")
st.title("📊 Şirket Puantaj ve Hak Ediş Otomasyonu")

if 'calisanlar' not in st.session_state:
    st.session_state.calisanlar = [
        {"id": 1, "ad_soyad": "FATİH GENÇOĞLU", "tur": "Yevmiye", "ucret": 2167, "banka_tutari": 15000, "giris_tarihi": "2026-09-01", "aktif": True},
        {"id": 2, "ad_soyad": "SANAYİ TOPRAK", "tur": "Yevmiye", "ucret": 1778, "banka_tutari": 15000, "giris_tarihi": "2026-09-01", "aktif": True},
        {"id": 3, "ad_soyad": "ENVER DEMİR", "tur": "Aylık", "ucret": 45700, "banka_tutari": 15000, "giris_tarihi": "2026-09-01", "aktif": True},
        {"id": 4, "ad_soyad": "OKAN ÇELİK", "tur": "Yevmiye", "ucret": 2094, "banka_tutari": 15000, "giris_tarihi": "2026-09-01", "aktif": True},
        {"id": 5, "ad_soyad": "MUSTAFA ÖZER", "tur": "Yevmiye", "ucret": 1460, "banka_tutari": 15000, "giris_tarihi": "2026-09-01", "aktif": True},
        {"id": 6, "ad_soyad": "MUSTAFA BAŞAR", "tur": "Yevmiye", "ucret": 1778, "banka_tutari": 15000, "giris_tarihi": "2026-09-01", "aktif": True},
        {"id": 7, "ad_soyad": "SADIK AYGÜN", "tur": "Aylık", "ucret": 60000, "banka_tutari": 15000, "giris_tarihi": "2026-09-03", "aktif": True},
        {"id": 8, "ad_soyad": "FIRAT SAYMAZ", "tur": "Aylık", "ucret": 110000, "banka_tutari": 15000, "giris_tarihi": "2026-09-01", "aktif": True},
        {"id": 9, "ad_soyad": "HAKAN ALTUNBULAT", "tur": "Aylık", "ucret": 140000, "banka_tutari": 15000, "giris_tarihi": "2026-09-01", "aktif": True}
    ]

if 'aylik_matris' not in st.session_state:
    st.session_state.aylik_matris = {}

st.sidebar.markdown("### 🏢 POLAY PUANTAJ")
menu = st.sidebar.radio("Sayfalar", ["📅 Puantaj Girişi", "👤 Çalışan Yönetimi", "💰 Maaş & Ödeme Raporu"])

gun_kisa_adlar = {0: "PZT", 1: "SAL", 2: "ÇAR", 3: "PER", 4: "CUM", 5: "CMT", 6: "PZ"}

if menu == "👤 Çalışan Yönetimi":
    st.subheader("➕ Yeni Çalışan Ekle")
    with st.form("yeni_calisan", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            ad = st.text_input("Adı Soyadı").upper()
            tur = st.selectbox("Maaş Tipi", ["Yevmiye", "Aylık"])
            ucret = st.number_input("Ücret Tutarı (Günlük/Aylık)", min_value=0, value=1000)
        with col2:
            banka_tutari = st.number_input("Bu İşçinin Bankaya Yatacak Sabit Tutarı", min_value=0, value=15000, step=1000)
            giris_tar = st.date_input("İşe Giriş Tarihi", datetime.now())
        submit = st.form_submit_button("💾 Çalışanı Sisteme Kaydet")
        if submit and ad:
            yeni_id = len(st.session_state.calisanlar) + 1
            st.session_state.calisanlar.append({"id": yeni_id, "ad_soyad": ad, "tur": tur, "ucret": ucret, "banka_tutari": banka_tutari, "giris_tarihi": giris_tar.strftime('%Y-%m-%d'), "aktif": True})
            st.success(f"✔️ {ad} başarıyla listeye eklendi!")
            st.rerun()

    st.write("---")
    st.subheader("✏️ Çalışan Bilgilerini Düzenle / Güncelle")
    aktif_isimler_duzenle = [c["ad_soyad"] for c in st.session_state.calisanlar if c["aktif"]]
    if aktif_isimler_duzenle:
        secilen_duzenle = st.selectbox("Bilgilerini değiştirmek istediğiniz çalışanı seçin:", aktif_isimler_duzenle, key="duzenle_sec")
        idx = next(i for i, c in enumerate(st.session_state.calisanlar) if c["ad_soyad"] == secilen_duzenle)
        calisan_bilgi = st.session_state.calisanlar[idx]
        with st.form("calisan_duzenle_form"):
            col1, col2 = st.columns(2)
            with col1:
                yeni_tur = st.selectbox("Yeni Maaş Tipi", ["Yevmiye", "Aylık"], index=["Yevmiye", "Aylık"].index(calisan_bilgi["tur"]))
                yeni_ucret = st.number_input("Yeni Ücret Tutarı", min_value=0, value=int(calisan_bilgi["ucret"]))
            with col2:
                yeni_banka = st.number_input("Yeni Banka Tutarı", min_value=0, value=int(calisan_bilgi["banka_tutari"]))
                yeni_giris = st.date_input("Yeni Giriş Tarihi", datetime.strptime(calisan_bilgi["giris_tarihi"], '%Y-%m-%d').date())
            guncelle_butonu = st.form_submit_button("🔄 Bilgileri Güncelle")
            if guncelle_butonu:
                st.session_state.calisanlar[idx]["tur"] = yeni_tur
                st.session_state.calisanlar[idx]["ucret"] = yeni_ucret
                st.session_state.calisanlar[idx]["banka_tutari"] = yeni_banka
                st.session_state.calisanlar[idx]["giris_tarihi"] = yeni_giris.strftime('%Y-%m-%d')
                st.success(f"✔️ {secilen_duzenle} isimli çalışanın bilgileri başarıyla güncellendi!")
                st.rerun()

    st.write("---")
    st.write("### 👥 Mevcut Çalışan Listesi")
    df_calisanlar = pd.DataFrame(st.session_state.calisanlar)
    if not df_calisanlar.empty:
        st.dataframe(df_calisanlar[df_calisanlar["aktif"] == True][["id", "ad_soyad", "tur", "ucret", "banka_tutari", "giris_tarihi"]], use_container_width=True)

    st.write("---")
    st.subheader("🗑️ Çalışan Sil")
    aktif_isimler = [c["ad_soyad"] for c in st.session_state.calisanlar if c["aktif"]]
    if aktif_isimler:
        secilen_sil = st.selectbox("Silmek istediğiniz çalışanı seçin:", aktif_isimler, key="sil_sec")
        sil_butonu = st.button("🚨 Seçilen Çalışanı Tamamen Sil")
        if sil_butonu:
            st.session_state.calisanlar = [c for c in st.session_state.calisanlar if c["ad_soyad"] != secilen_sil]
            st.success(f"❌ {secilen_sil} sistemden kalıcı olarak temizlendi!")
            st.rerun()

elif menu == "📅 Puantaj Girişi":
    st.subheader("📅 Tüm Ayı Gösteren Puantaj Tablosu")
    col_y, col_a = st.columns(2)
    with col_y:
        secilen_yil = st.selectbox("Yıl", [2026, 2027, 2028])
    with col_a:
        secilen_ay = st.selectbox("Ay", ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"], index=8)
    
    ay_numaralari = {"Ocak":1,"Şubat":2,"Mart":3,"Nisan":4,"Mayıs":5,"Haziran":6,"Temmuz":7,"Ağustos":8,"Eylül":9,"Ekim":10,"Kasım":11,"Aralık":12}
    ay_no = ay_numaralari[secilen_ay]
    weekday, gun_sayisi = calendar.monthrange(secilen_yil, ay_no)
    st.info("💡 Kullanım: Hücrelerin içine çift tıklayarak kodları (1, 0, 2, Ç) yazın. İşlem bitince alttaki kaydet butonuna basın.")
    
    matris_data = []
    sutun_haritalama = {}
    
    for c in st.session_state.calisanlar:
        if c["aktif"]:
            satir = {"SIRA": c["id"], "ADI SOYADI": c["ad_soyad"]}
            for gun in range(1, gun_sayisi + 1):
                try:
                    wd = datetime(secilen_yil, ay_no, gun).weekday()
                except:
                    wd = 0
                s_adi = f"{gun} {gun_kisa_adlar[wd]}"
                sutun_haritalama[gun] = s_adi
                matris_key = f"{secilen_yil}_{ay_no}_{c['id']}_{gun}"
                if matris_key not in st.session_state.aylik_matris:
                    st.session_state.aylik_matris[matris_key] = ""
                satir[s_adi] = st.session_state.aylik_matris[matris_key]
            matris_data.append(satir)

    if matris_data:
        df_matris = pd.DataFrame(matris_data)
        guncel_tablo = st.data_editor(df_matris, hide_index=True, disabled=["SIRA", "ADI SOYADI"], use_container_width=True)
        if st.button("💾 Tüm Aylık Puantaj Değişikliklerini Kaydet"):
            for _, row in guncel_tablo.iterrows():
                c_id = row["SIRA"]
                for gun in range(1, gun_sayisi + 1):
                    s_adi = sutun_haritalama[gun]
                    matris_key = f"{secilen_yil}_{ay_no}_{c_id}_{gun}"
                    st.session_state.aylik_matris[matris_key] = str(row[s_adi]).strip()
            st.success(f"✔️ {secilen_ay} {secilen_yil} dönemine ait tüm puantaj tablosu başarıyla kaydedildi!")

elif menu == "💰 Maaş & Ödeme Raporu":
    st.subheader("Hak Ediş ve Ödeme Dağılım Listesi")
    col_ry, col_ra = st.columns(2)
    with col_ry:
        r_yil = st.selectbox("Rapor Yılı", [2026, 2027, 2028])
    with col_ra:
        r_ay = st.selectbox("Rapor Ayı", ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"], index=8)
    
    ay_numaralari = {"Ocak":1,"Şubat":2,"Mart":3,"Nisan":4,"Mayıs":5,"Haziran":6,"Temmuz":7,"Ağustos":8,"Eylül":9,"Ekim":10,"Kasım":11,"Aralık":12}
    r_ay_no = ay_numaralari[r_ay]
    weekday, r_gun_sayisi = calendar.monthrange(r_yil, r_ay_no)

    rapor_verisi = []
    for c in st.session_state.calisanlar:
        if c["aktif"]:
            toplam_yevmiye = 0
            is_cikis_yapti = False
            haftalik_calisma = {}
            pazar_gunleri = []
            giris_tarihi_obj = datetime.strptime(c["giris_tarihi"], '%Y-%m-%d').date()
            
            for gun in range(1, r_gun_sayisi + 1):
                try:
                    mevcut_tarih = datetime(r_yil, r_ay_no, gun).date()
                except:
                    continue
                matris_key = f"{r_yil}_{r_ay_no}_{c['id']}_{gun}"
                v = st.session_state.aylik_matris.get(matris_key, "").strip()
                if mevcut_tarih < giris_tarihi_obj or is_cikis_yapti:
                    continue
                if v == "Ç":
                    is_cikis_yapti = True
                    continue
                
                hafta_key = mevcut_tarih.strftime('%Y-W%U')
                if hafta_key not in haftalik_calisma:
                    haftalik_calisma[hafta_key] = 0
                
                if mevcut_tarih.weekday() == 6:
                    pazar_gunleri.append({"hafta_key": hafta_key, "kod": v})
                else:
                    if v == "1":
                        toplam_yevmiye += 1
                        haftalik_calisma[hafta_key] += 1
                    elif v == "2":
                        toplam_yevmiye += 2
