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
gecerli_kodlar = ["1", "0", "2", "Ç"]

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
    st.subheader("📅 Şerit Tipi Aylık Puantaj Giriş Paneli")
    col_y, col_a = st.columns(2)
    with col_y: secilen_yil = st.selectbox("Yıl", [2026, 2027])
    with col_a: secilen_ay = st.selectbox("Ay", ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"], index=8)
    
    ay_no = {"Ocak":1,"Şubat":2,"Mart":3,"Nisan":4,"Mayıs":5,"Haziran":6,"Temmuz":7,"Ağustos":8,"Eylül":9,"Ekim":10,"Kasım":11,"Aralık":12}[secilen_ay]
    weekday, gun_sayisi = calendar.monthrange(secilen_yil, ay_no)
    
    st.warning("💡 Önemli İpucu: Her çalışanın yanındaki kutuya o ayki puantaj kodlarını aralarında birer boşluk bırakarak sırayla yazın (Örn: 1 1 1 0 2 1 Ç). Hatalı girilen her karakter mor butona basıldığında otomatik silinir.")
    
    gecici_girdiler = {}
    with st.form("serit_puantaj_form"):
        for c in st.session_state.calisanlar:
            if c["aktif"]:
                eski_liste = [st.session_state.aylik_matris.get(f"{secilen_yil}_{ay_no}_{c['id']}_{g}", "") for gun in range(1, gun_sayisi + 1)]
                eski_metin = " ".join([v for v in eski_liste if v != ""])
                gecici_girdiler[c["id"]] = st.text_input(f"👤 {c['ad_soyad']} ({c['tur']}) - Toplam {gun_sayisi} Gün", value=eski_metin, key=f"inp_{c['id']}")
        
        if st.form_submit_button("💾 Tüm Aylık Puantaj Değişikliklerini Kaydet"):
            for c_id, metin in gecici_girdiler.items():
                parcalar = [p.strip().upper() for p in metin.split(" ") if p.strip() != ""]
                for gun in range(1, gun_sayisi + 1):
                    matris_key = f"{secilen_yil}_{ay_no}_{c_id}_{gun}"
                    if (gun - 1) < len(parcalar):
                        kod = parcalar[gun - 1]
                        st.session_state.aylik_matris[matris_key] = kod if kod in gecerli_kodlar else ""
                    else:
                        st.session_state.aylik_matris[matris_key] = ""
            st.success("✔️ Tüm şeritler analiz edildi, hatalı girişler kazındı ve kaydedildi!")
            st.rerun()

elif menu == "💰 Maaş & Ödeme Raporu":
    st.subheader("Hak Ediş ve Ödeme Dağılım Listesi")
    col_ry, col_ra = st.columns(2)
    with col_ry: r_yil = st.selectbox("Rapor Yılı", [2026, 2027])
    with col_ra: r_ay = st.selectbox("Rapor Ayı", ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"], index=8)
    
    r_ay_no = {"Ocak":1,"Şubat":2,"Mart":3,"Nisan":4,"Mayıs":5,"Haziran":6,"Temmuz":7,"Ağustos":8,"Eylül":9,"Ekim":10,"Kasım":11,"Aralık":12}[r_ay]
    weekday, r_gun_sayisi = calendar.monthrange(r_yil, r_ay_no)
    rapor_verisi = []

    for c in st.session_state.calisanlar:
        if c["aktif"]:
            toplam_yevmiye, is_cikis, haftalik_calisma, pazar_gunleri = 0, False, {}, []
            giris_tarihi_obj = datetime.strptime(c["giris_tarihi"], '%Y-%m-%d').date()
            for gun in range(1, r_gun_sayisi + 1):
                try: m_tarih = datetime(r_yil, r_ay_no, gun).date()
                except: continue
                v = st.session_state.aylik_matris.get(f"{r_yil}_{r_ay_no}_{c['id']}_{gun}", "").strip().upper()
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
            rapor_verisi.append({"İşçi Adı": c["ad_soyad"], "Tür": c["tur"], "Çalışılan Gün": toplam_yevmiye, "Toplam Hak Ediş": f"{hak_edis:,.2f} ₺", "Bankaya Yatacak": f"{banka:,.2f} ₺", "Elden Verilecek": f"{(hak_edis - banka):,.2f} ₺"})
            
    if len(rapor_verisi) > 0:
        st.table(pd.DataFrame(rapor_verisi))
    else:
        st.write("⚠️ Bu döneme ait girilmiş puantaj verisi bulunamadı.")
