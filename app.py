import streamlit as st
import pandas as pd
from datetime import datetime
import calendar

st.set_page_config(page_title="Polay Puantaj Sistemi", layout="wide", initial_sidebar_state="expanded")
st.title("📊 Şirket Puantaj ve Hak Ediş Otomasyonu")

if 'calisanlar' not in st.session_state:
    st.session_state.calisanlar = [
        {"id": 1, "ad_soyad": "FATİH GENÇOĞLU", "tur": "Yevmiye", "ucret": 2167, "banka_tutari": 34750, "giris_tarihi": "2026-09-01", "aktif": True},
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
gecerli_kodlar = ["1", "0", "2", "Ç", ""]
secilen_yil = 2026

if menu == "👤 Çalışan Yönetimi":
    st.subheader("➕ Yeni Çalışan Ekle")
    with st.form("yeni_calisan", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            ad = st.text_input("Adı Soyadı").upper()
            tur = st.selectbox("Maaş Tipi", ["Yevmiye", "Aylık"])
            ucret = st.number_input("Ücret Tutarı", min_value=0, value=1000)
        with col2:
            banka_tutari = st.number_input("Bankaya Yatacak Sabit Tutar", min_value=0, value=15000, step=1000)
            giris_tar = st.date_input("İşe Giriş Tarihi", datetime.now())
        if st.form_submit_button("💾 Çalışanı Sisteme Kaydet") and ad:
            yeni_id = len(st.session_state.calisanlar) + 1
            st.session_state.calisanlar.append({"id": yeni_id, "ad_soyad": ad, "tur": tur, "ucret": ucret, "banka_tutari": banka_tutari, "giris_tarihi": giris_tar.strftime('%Y-%m-%d'), "aktif": True})
            st.success("✔️ Eklendi!")
            st.rerun()

    st.write("---")
    st.subheader("✏️ Çalışan Bilgilerini Düzenle / Güncelle")
    aktif_isimler_duzenle = [c["ad_soyad"] for c in st.session_state.calisanlar if c["aktif"]]
    if aktif_isimler_duzenle:
        secilen_duzenle = st.selectbox("Çalışan Seçin:", aktif_isimler_duzenle, key="duzenle_sec")
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
            if st.form_submit_button("🔄 Bilgileri Güncelle"):
                st.session_state.calisanlar[idx]["tur"] = yeni_tur
                st.session_state.calisanlar[idx]["ucret"] = yeni_ucret
                st.session_state.calisanlar[idx]["banka_tutari"] = yeni_banka
                st.session_state.calisanlar[idx]["giris_tarihi"] = yeni_giris.strftime('%Y-%m-%d')
                st.success("✔️ Güncellendi!")
                st.rerun()

    st.write("---")
    st.subheader("🗑️ Çalışan Sil")
    aktif_isimler = [c["ad_soyad"] for c in st.session_state.calisanlar if c["aktif"]]
    if aktif_isimler:
        secilen_sil = st.selectbox("Silmek istediğiniz çalışanı seçin:", aktif_isimler, key="sil_sec")
        if st.button("🚨 Seçilen Çalışanı Tamamen Sil"):
            st.session_state.calisanlar = [c for c in st.session_state.calisanlar if c["ad_soyad"] != secilen_sil]
            st.success("❌ Silindi!")
            st.rerun()

elif menu == "📅 Puantaj Girişi":
    st.subheader("📅 Tüm Ayı Gösteren Puantaj Tablosu")
    secilen_ay = st.selectbox("Ay Seçin", ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"], index=8)
    ay_no = {"Ocak":1,"Şubat":2,"Mart":3,"Nisan":4,"Mayıs":5,"Haziran":6,"Temmuz":7,"Ağustos":8,"Eylül":9,"Ekim":10,"Kasım":11,"Aralık":12}[secilen_ay]
    weekday, gun_sayisi = calendar.monthrange(secilen_yil, ay_no)
    st.info("💡 Kullanım: Hücrelere klavyeden doğrudan yazabilirsiniz. Hatalı kodlar kaydederken otomatik temizlenir.")
    
    matris_data = list()
    sutun_haritalama = dict()
    config_sutunlar = {"SIRA": st.column_config.NumberColumn(disabled=True), "ADI SOYADI": st.column_config.TextColumn(disabled=True)}
    
    for c in st.session_state.calisanlar:
        if c["aktif"]:
            satir = {"SIRA": int(c["id"]), "ADI SOYADI": str(c["ad_soyad"])}
            for gun in range(1, gun_sayisi + 1):
                try: wd = datetime(secilen_yil, ay_no, gun).weekday()
                except: wd = 0
                s_adi = f"{gun} {gun_kisa_adlar[wd]}"
                sutun_haritalama[gun] = s_adi
                config_sutunlar[s_adi] = st.column_config.TextColumn(width="small")
                matris_key = f"{secilen_yil}_{ay_no}_{c['id']}_{gun}"
                if matris_key not in st.session_state.aylik_matris: st.session_state.aylik_matris[matris_key] = ""
                satir[s_adi] = st.session_state.aylik_matris[matris_key]
            matris_data.append(satir)

    if matris_data:
        df_matris = pd.DataFrame(matris_data)
        guncel_tablo = st.data_editor(df_matris, hide_index=True, column_config=config_sutunlar, use_container_width=True, key=f"matris_v_final_{secilen_yil}_{ay_no}")
        if st.button("💾 Tüm Aylık Puantaj Değişikliklerini Kaydet"):
            for _, row in guncel_tablo.iterrows():
                c_id = int(row["SIRA"])
                for gun in range(1, gun_sayisi + 1):
                    s_adi = sutun_haritalama[gun]
                    girilen_deger = str(row[s_adi]).strip().upper()
                    matris_key = f"{secilen_yil}_{ay_no}_{c_id}_{gun}"
                    st.session_state.aylik_matris[matris_key] = girilen_deger if girilen_deger in gecerli_kodlar else ""
            st.success("✔️ Kaydedildi!")
            st.rerun()

elif menu == "💰 Maaş & Ödeme Raporu":
    st.subheader("Hak Ediş ve Ödeme Dağılım Listesi")
    r_ay = st.selectbox("Rapor Ayı Seçin", ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"], index=8)
    r_ay_no = {"Ocak":1,"Şubat":2,"Mart":3,"Nisan":4,"Mayıs":5,"Haziran":6,"Temmuz":7,"Ağustos":8,"Eylül":9,"Ekim":10,"Kasım":11,"Aralık":12}[r_ay]
    weekday, r_gun_sayisi = calendar.monthrange(secilen_yil, r_ay_no)
    
    rapor_verisi = list()
    top_hakedis, top_banka, top_elden = 0.0, 0.0, 0.0

    for c in st.session_state.calisanlar:
        if c["aktif"]:
            toplam_yevmiye, is_cikis, haftalik_calisma, pazar_gunleri = 0, False, dict(), list()
            giris_tarihi_obj = datetime.strptime(c["giris_tarihi"], '%Y-%m-%d').date()
            for gun in range(1, r_gun_sayisi + 1):
                try: m_tarih = datetime(secilen_yil, r_ay_no, gun).date()
                except: continue
                v = st.session_state.aylik_matris.get(f"{secilen_yil}_{r_ay_no}_{c['id']}_{gun}", "").strip().upper()
                if m_tarih < giris_tarihi_obj or is_cikis: continue
                if v == "Ç": is_cikis = True; continue
                h_key = m_tarih.strftime('%Y-W%U')
                if h_key not in haftalik_calisma: haftalik_calisma[h_key] = 0
                if m_tarih.weekday() == 6: pazar_gunleri.append({"h_key": h_key, "kod": v})
                else:
                    if v == "1": toplam_yevmiye += 1; haftalik_calisma[h_key] += 1
                    elif v == "2": toplam_yevmiye += 2; haftalik_calisma[h_key] += 1
            for pzr in pazar_gunleri:
                if pzr["kod"] == "1": toplam_yevmiye += 1
                elif pzr["kod"] == "2": toplam_yevmiye += 2
                elif haftalik_calisma.get(pzr["h_key"], 0) >= 4: toplam_yevmiye += 1
            
            hak_edis = float(toplam_yevmiye * c["ucret"]) if c["tur"] == "Yevmiye" else (float(c["ucret"]) if not is_cikis else float(c["ucret"] / 2))
            banka = min(float(c["banka_tutari"]), float(hak_edis))
            elden = float(hak_edis - banka)
            
            top_hakedis += hak_edis
            top_banka += banka
            top_elden += elden
            
            rapor_verisi.append({
                "İşçi Adı": c["ad_soyad"], "Tür": c["tur"], "Çal. Gün": toplam_yevmiye,
                "Toplam Hak Ediş": f"{hak_edis:,.2f} ₺", "Bankaya Yatacak": f"{banka:,.2f} ₺", "Elden Verilecek": f"{elden:,.2f} ₺"
