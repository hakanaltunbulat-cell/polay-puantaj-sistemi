import streamlit as st
import pandas as pd
from datetime import datetime
import calendar
import json
import os

# ---------------------------------------------------------
# KALICI VERİ DEPOLAMA SİSTEMİ (JSON VERİTABANI)
# ---------------------------------------------------------
VERI_DOSYASI = "veritabani.json"

def verileri_yukle():
    if os.path.exists(VERI_DOSYASI):
        with open(VERI_DOSYASI, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # Varsayılan ilk kurulum verileri
        return {
            "calisanlar": [
                {"id": 1, "ad_soyad": "FATİH GENÇOĞLU", "tur": "Yevmiye", "ucret": 2167, "banka_tutari": 34750},
                {"id": 2, "ad_soyad": "SANAYİ TOPRAK", "tur": "Yevmiye", "ucret": 1778, "banka_tutari": 15000},
                {"id": 3, "ad_soyad": "ENVER DEMİR", "tur": "Yevmiye", "ucret": 1524, "banka_tutari": 15000},
                {"id": 4, "ad_soyad": "OKAN ÇELİK", "tur": "Yevmiye", "ucret": 2167, "banka_tutari": 15000},
                {"id": 5, "ad_soyad": "MUSTAFA ÖZER", "tur": "Yevmiye", "ucret": 1905, "banka_tutari": 15000},
                {"id": 6, "ad_soyad": "MUSTAFA BAŞAR", "tur": "Yevmiye", "ucret": 1905, "banka_tutari": 15000},
                {"id": 7, "ad_soyad": "SADIK AYGÜN", "tur": "Yevmiye", "ucret": 2000, "banka_tutari": 15000},
                {"id": 8, "ad_soyad": "FIRAT SAYMAZ", "tur": "Aylık", "ucret": 110000, "banka_tutari": 15000},
                {"id": 9, "ad_soyad": "HAKAN ALTUNBULAT", "tur": "Aylık", "ucret": 140000, "banka_tutari": 15000}
            ],
            "aylik_matris": {}
        }

def verileri_kaydet():
    veri = {
        "calisanlar": st.session_state.calisanlar,
        "aylik_matris": st.session_state.aylik_matris
    }
    with open(VERI_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=4)

# ---------------------------------------------------------
# UYGULAMA BAŞLANGICI VE OTURUM YÖNETİMİ
# ---------------------------------------------------------
KULLANICI_ADI, SIFRE = "polay", "1234"
st.set_page_config(page_title="Polay Madencilik Puantaj", layout="wide")

if 'giris_yapildi' not in st.session_state: 
    st.session_state.giris_yapildi = False

# Kalıcı verileri session_state içerisine aktar
if 'calisanlar' not in st.session_state or 'aylik_matris' not in st.session_state:
    kayitli_veri = verileri_yukle()
    st.session_state.calisanlar = kayitli_veri["calisanlar"]
    st.session_state.aylik_matris = kayitli_veri["aylik_matris"]

# Güvenli Giriş Ekranı
if not st.session_state.giris_yapildi:
    st.subheader("🔒 POLAY PUANTAJ SİSTEMİ - GÜVENLİ GİRİŞ")
    g_kullanici = st.text_input("Yönetici Kullanıcı Adı:")
    g_sifre = st.text_input("Giriş Şifresi:", type="password")
    if st.button("🔓 Sisteme Güvenli Giriş Yap"):
        if g_kullanici == KULLANICI_ADI and g_sifre == SIFRE:
            st.session_state.giris_yapildi = True
            st.success("Giriş Başarılı!")
            st.rerun()
        else: 
            st.error("🚨 Hatalı Giriş Bilgileri!")
    st.stop()

# Tasarım Düzenlemeleri (CSS)
st.markdown("""<style>
    .excel-title { background-color: #75aadb !important; color: black !important; text-align: center; font-weight: bold; font-size: 20px; padding: 12px; border: 1px solid black; margin-bottom: 25px; }
    th { background-color: #bdd7ee !important; color: black !important; border: 1px solid black !important; text-align: center !important; }
    td { border: 1px solid #d9d9d9 !important; text-align: center !important; }
</style>""", unsafe_allow_html=True)

st.markdown('<div class="excel-title">POLAY MADENCİLİK DİNAMİK PUANTAJ SİSTEMİ</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# SOL PANEL (YÖNETİM PANELI & TARİH SEÇİMİ)
# ---------------------------------------------------------
st.sidebar.markdown("### 🏢 YÖNETİM PANELİ")
if st.sidebar.button("🔒 Güvenli Çıkış Yap"): 
    st.session_state.giris_yapildi = False
    st.rerun()

islem = st.sidebar.radio("İşlem Seçin", ["📅 Puantaj Matrisi & Rapor", "👤 Çalışan Ekle / Sil / Düzenle"])

# Dinamik Takvim Ayarları
st.sidebar.markdown("---")
st.sidebar.markdown("### 📆 Dönem / Takvim Seçimi")
aylar_tr = {
    1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran",
    7: "Temmuz", 8: "Ağustos", 9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık"
}
simdiki_yil = datetime.now().year
secilen_yil = st.sidebar.selectbox("Yıl Seçin", list(range(simdiki_yil - 2, simdiki_yil + 3)), index=2)
ay_no = st.sidebar.selectbox("Ay Seçin", list(aylar_tr.keys()), format_func=lambda x: aylar_tr[x], index=8) # Varsayılan Eylül
secilen_ay = aylar_tr[ay_no]

# Seçilen aya göre gün sayısını dinamik bulma
gun_sayisi = calendar.monthrange(secilen_yil, ay_no)[1]
gun_kisa_adlar = {0: "PZT", 1: "SAL", 2: "ÇAR", 3: "PER", 4: "CUM", 5: "CMT", 6: "PZ"}
gecerli_kodlar = ["1", "0", "2", "Ç", ""]

# ---------------------------------------------------------
# SAYFA 1: ÇALIŞAN EKLE / SİL / DÜZENLE
# ---------------------------------------------------------
if islem == "👤 Çalışan Ekle / Sil / Düzenle":
    st.subheader("👤 Çalışan Listesi ve Banka Bilgisi Yönetimi")
    
    # Ekleme Bölümü
    st.markdown("### ➕ Yeni Çalışan Ekle")
    ad = st.text_input("Yeni Çalışan Adı Soyadı").upper()
    tur = st.selectbox("Maaş Tipi", ["Yevmiye", "Aylık"])
    ucret = st.number_input("Ücret Tutarı", min_value=0, value=2000)
    b_tut = st.number_input("Bankaya Yatacak Sabit Tutar", min_value=0, value=15000)
    
    if st.button("💾 Yeni Çalışanı Sisteme Kaydet") and ad:
        y_id = max([c["id"] for c in st.session_state.calisanlar]) + 1 if st.session_state.calisanlar else 1
        st.session_state.calisanlar.append({"id": y_id, "ad_soyad": ad, "tur": tur, "ucret": ucret, "banka_tutari": b_tut})
        verileri_kaydet()
        st.success("✔️ Personel başarıyla eklendi ve kalıcı olarak kaydedildi!"); st.rerun()
        
    st.write("---")
    
    # Güncelleme Bölümü
    isimler = [c["ad_soyad"] for c in st.session_state.calisanlar]
    if Black_list := list(set(isimler)):
        st.markdown("### 🔄 Personel Kartı Güncelle")
        secilen_kisi = st.selectbox("Bilgilerini Güncelleyeceğiniz Personeli Seçin:", Black_list)
        idx = next(i for i, c in enumerate(st.session_state.calisanlar) if c["ad_soyad"] == secilen_kisi)
        
        y_ucret = st.number_input("Güncel Ücret / Yevmiye (₺)", min_value=0, value=int(st.session_state.calisanlar[idx]["ucret"]))
        y_banka = st.number_input("Güncel Bankaya Yatacak Sabit Tutar (₺)", min_value=0, value=int(st.session_state.calisanlar[idx]["banka_tutari"]))
        
        if st.button("🔄 Değişiklikleri Personel Kartına Kilitle"):
            st.session_state.calisanlar[idx]["ucret"] = y_ucret
            st.session_state.calisanlar[idx]["banka_tutari"] = y_banka
            verileri_kaydet()
            st.success("✔️ Değişiklikler başarıyla güncellendi ve kaydedildi!"); st.rerun()
            
    st.write("---")
    
    # Silme Bölümü
    if isimler:
        st.markdown("### 🚨 Personel Silme İşlemi")
        sil_ad = st.selectbox("Sistemden Silinecek Çalışanı Seçin:", list(set(isimler)), key="silme_box")
        if st.button("🚨 Seçilen Çalışanı Tamamen Sil"):
            st.session_state.calisanlar = [c for c in st.session_state.calisanlar if c["ad_soyad"] != sil_ad]
            verileri_kaydet()
            st.success("❌ Çalışan sistemden kaldırıldı ve veritabanı güncellendi!"); st.rerun()

# ---------------------------------------------------------
# SAYFA 2: PUANTAJ MATRİSİ & RAPORLAR
# ---------------------------------------------------------
elif islem == "📅 Puantaj Matrisi & Rapor":
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧨 Ateşçi Ödeneği Ayarları")
    aktif_isimler = [c["ad_soyad"] for c in st.session_state.calisanlar]
    secilen_atesci = st.sidebar.selectbox("Bu Ayki Ateşçi Kim?", ["Hiçbiri"] + aktif_isimler, index=0)
    atesci_ucreti = st.sidebar.number_input("Ateşçi Ödenek Tutarı (₺)", min_value=0, value=30000, step=5000)
    
    matris_data = list()
    sutun_haritalama = dict()
    config_sutunlar = {
        "SIRA": st.column_config.NumberColumn(disabled=True), 
        "ADI SOYADI": st.column_config.TextColumn(disabled=True)
    }
    
    # Matris Satır/Sütun Yapısının İnşası
    for c in st.session_state.calisanlar:
        satir = {"SIRA": int(c["id"]), "ADI SOYADI": str(c["ad_soyad"])}
        for gun in range(1, gun_sayisi + 1):
            try: 
                wd = datetime(secilen_yil, ay_no, gun).weekday()
            except: 
                wd = 0
            s_adi = f"{gun} {gun_kisa_adlar[wd]}"
            sutun_haritalama[gun] = s_adi
            config_sutunlar[s_adi] = st.column_config.TextColumn(width="small")
            
            # Dinamik Anahtar: Yıl_Ay_KişiID_Gün
            m_key = f"{secilen_yil}_{ay_no}_{c['id']}_{gun}"
            if m_key not in st.session_state.aylik_matris: 
                st.session_state.aylik_matris[m_key] = ""
            satir[s_adi] = st.session_state.aylik_matris[m_key]
        matris_data.append(satir)
        
    # Tablonun Ekranda Gösterilmesi
    if matris_data:
        df_matris = pd.DataFrame(matris_data)
        g_tablo = st.data_editor(df_matris, hide_index=True, column_config=config_sutunlar, use_container_width=True, key="m_ed_v_f")
        
        if st.button("💾 Bu Ayın Puantaj Değişikliklerini Kaydet"):
            for _, row in g_tablo.iterrows():
                c_id = int(row["SIRA"])
                for gun in range(1, gun_sayisi + 1):
                    deger = str(row[sutun_haritalama[gun]]).strip().upper()
                    st.session_state.aylik_matris[f"{secilen_yil}_{ay_no}_{c_id}_{gun}"] = deger if deger in gecerli_kodlar else ""
            verileri_kaydet()
