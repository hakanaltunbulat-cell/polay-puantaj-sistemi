import streamlit as st
import pandas as pd
from datetime import datetime
import calendar
import json
import os

# --- GÜVENLİK VE DOSYA YAPILANDIRMASI ---
KULLANICI_ADI, SIFRE = "polay", "1234"
CALISAN_DOSYA, MATRIS_DOSYA = "veri_calisanlar.json", "veri_puantaj.json"

st.set_page_config(page_title="Polay Madencilik Puantaj", layout="wide")

# Oturum Durumu Kontrolü
if 'giris_yapildi' not in st.session_state: 
    st.session_state.giris_yapildi = False

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

# Veri Dosyalarının Yüklenmesi
if 'calisanlar' not in st.session_state or 'aylik_matris' not in st.session_state:
    if os.path.exists(CALISAN_DOSYA):
        with open(CALISAN_DOSYA, "r", encoding="utf-8") as f: 
            st.session_state.calisanlar = json.load(f)
    else:
        st.session_state.calisanlar = [
            {"id": 1, "ad_soyad": "FATİH GENÇOĞLU", "tur": "Yevmiye", "ucret": 2167, "banka_tutari": 34750},
            {"id": 2, "ad_soyad": "SANAYİ TOPRAK", "tur": "Yevmiye", "ucret": 1778, "banka_tutari": 15000},
            {"id": 3, "ad_soyad": "ENVER DEMİR", "tur": "Yevmiye", "ucret": 1524, "banka_tutari": 15000},
            {"id": 4, "ad_soyad": "OKAN ÇELİK", "tur": "Yevmiye", "ucret": 2167, "banka_tutari": 15000},
            {"id": 5, "ad_soyad": "MUSTAFA ÖZER", "tur": "Yevmiye", "ucret": 1905, "banka_tutari": 15000},
            {"id": 6, "ad_soyad": "MUSTAFA BAŞAR", "tur": "Yevmiye", "ucret": 1905, "banka_tutari": 15000},
            {"id": 7, "ad_soyad": "SADIK AYGÜN", "tur": "Yevmiye", "ucret": 2000, "banka_tutari": 15000},
            {"id": 8, "ad_soyad": "FIRAT SAYMAZ", "tur": "Aylık", "ucret": 110000, "banka_tutari": 15000},
            {"id": 9, "ad_soyad": "HAKAN ALTUNBULAT", "tur": "Aylık", "ucret": 140000, "banka_tutari": 15000}
        ]
    
    if os.path.exists(MATRIS_DOSYA):
        with open(MATRIS_DOSYA, "r", encoding="utf-8") as f: 
            st.session_state.aylik_matris = json.load(f)
    else:
        st.session_state.aylik_matris = {}
        for c in st.session_state.calisanlar:
            for g in range(1, 31): 
                st.session_state.aylik_matris[f"2026_9_{c['id']}_{g}"] = "1"
            st.session_state.aylik_matris[f"2026_9_{c['id']}_11"] = "0"
            st.session_state.aylik_matris[f"2026_9_{c['id']}_17"] = "0"
            st.session_state.aylik_matris[f"2026_9_{c['id']}_25"] = "0"

def verileri_kaydet():
    with open(CALISAN_DOSYA, "w", encoding="utf-8") as f: 
        json.dump(st.session_state.calisanlar, f, ensure_ascii=False, indent=4)
    with open(MATRIS_DOSYA, "w", encoding="utf-8") as f: 
        json.dump(st.session_state.aylik_matris, f, ensure_ascii=False, indent=4)

# --- ARAYÜZ VE GÖRSEL STİLLER (CSS) ---
st.markdown("""<style>
    .excel-title { background-color: #75aadb !important; color: black !important; text-align: center; font-weight: bold; font-size: 20px; padding: 12px; border: 1px solid black; margin-bottom: 15px; }
    th { background-color: #bdd7ee !important; color: black !important; border: 1px solid black !important; text-align: center !important; }
    td { border: 1px solid #d9d9d9 !important; text-align: center !important; }
</style>""", unsafe_allow_html=True)

st.markdown('<div class="excel-title">POLAY MADENCİLİK DİNAMİK PUANTAJ SİSTEMİ</div>', unsafe_allow_html=True)

# --- YAN MENÜ (SIDEBAR) ---
st.sidebar.markdown("### 🏢 YÖNETİM PANELİ")
if st.sidebar.button("🔒 Güvenli Çıkış Yap"): 
    st.session_state.giris_yapildi = False
    st.rerun()

islem = st.sidebar.radio("İşlem Seçin", ["📅 Puantaj Matrisi & Rapor", "👤 Çalışan Ekle / Sil / Düzenle"])
gun_kisa_adlar = {0: "PZT", 1: "SAL", 2: "ÇAR", 3: "PER", 4: "CUM", 5: "CMT", 6: "PZ"}
gecerli_kodlar = ["1", "0", "2", "Ç", ""]

# --- MODÜL 1: ÇALIŞAN YÖNETİMİ ---
if islem == "👤 Çalışan Ekle / Sil / Düzenle":
    st.subheader("👤 Çalışan Listesi ve Banka Bilgisi Yönetimi")
    
    col1, col2 = st.columns(2)
    with col1:
        ad = st.text_input("Yeni Çalışan Adı Soyadı:").upper()
        tur = st.selectbox("Maaş Tipi:", ["Yevmiye", "Aylık"])
    with col2:
        ucret = st.number_input("Ücret / Maaş Tutarı (₺):", min_value=0, value=2000)
        b_tut = st.number_input("Bankaya Yatacak Sabit Tutar (₺):", min_value=0, value=15000)
        
    if st.button("💾 Yeni Çalışanı Sisteme Kaydet") and ad:
        y_id = max([c["id"] for c in st.session_state.calisanlar]) + 1 if st.session_state.calisanlar else 1
        st.session_state.calisanlar.append({"id": y_id, "ad_soyad": ad, "tur": tur, "ucret": ucret, "banka_tutari": b_tut})
        verileri_kaydet()
        st.success(f"✔️ {ad} başarıyla eklendi!")
        st.rerun()
        
    st.write("---")
    st.subheader("✏️ Personel Kartı Güncelleme")
    isimler = [c["ad_soyad"] for c in st.session_state.calisanlar]
    if isimler:
        secilen_kisi = st.selectbox("Personel Seçin:", list(set(isimler)))
        idx = next(i for i, c in enumerate(st.session_state.calisanlar) if c["ad_soyad"] == secilen_kisi)
        
        c_col1, c_col2 = st.columns(2)
        with c_col1:
            y_ucret = st.number_input("Güncel Ücret / Yevmiye (₺):", min_value=0, value=int(st.session_state.calisanlar[idx]["ucret"]))
        with c_col2:
            y_banka = st.number_input("Güncel Bankaya Yatacak Sabit Tutar (₺):", min_value=0, value=int(st.session_state.calisanlar[idx]["banka_tutari"]))
            
        if st.button("🔄 Değişiklikleri Personel Kartına Kilitle"):
            st.session_state.calisanlar[idx]["ucret"] = y_ucret
            st.session_state.calisanlar[idx]["banka_tutari"] = y_banka
            verileri_kaydet()
            st.success("✔️ Bilgiler başarıyla güncellendi!")
            st.rerun()
            
    st.write("---")
    st.subheader("🚨 Personel Kartı Silme")
    if isimler:
        sil_ad = st.selectbox("Sistemden Silinecek Çalışanı Seçin:", list(set(isimler)), key="sil_box")
        if st.button("🚨 Seçilen Çalışanı Tamamen Sil"):
            st.session_state.calisanlar = [c for c in st.session_state.calisanlar if c["ad_soyad"] != sil_ad]
            verileri_kaydet()
            st.success("❌ Personel kaydı silindi!")
            st.rerun()

# --- MODÜL 2: PUANTAJ MATRİSİ VE RAPORLAMA ---
elif islem == "📅 Puantaj Matrisi & Rapor":
    st.markdown("### 📅 Dönem Seçimi")
    c_y, c_a = st.columns(2)
    with c_y: secilen_yil = st.selectbox("Yıl Seçin", [2024, 2025, 2026, 2027], index=2)
    with c_a: secilen_ay = st.selectbox("Ay Seçin", ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"], index=8)
        
    ay_no = {"Ocak":1,"Şubat":2,"Mart":3,"Nisan":4,"Mayıs":5,"Haziran":6,"Temmuz":7,"Ağustos":8,"Eylül":9,"Ekim":10,"Kasım":11,"Aralık":12}[secilen_ay]
    weekday, gun_sayisi = calendar.monthrange(secilen_yil, ay_no)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧨 Ateşçi Ödeneği Ayarları")
    aktif_isimler = [c["ad_soyad"] for c in st.session_state.calisanlar]
    secilen_atesci = st.sidebar.selectbox("Bu Ayki Ateşçi Kim?", ["Hiçbiri"] + aktif_isimler, index=0)
    atesci_ucreti = st.sidebar.number_input("Ateşçi Ödenek Tutarı (₺)", min_value=0, value=30000, step=5000)
    
    matris_data = []
    sutun_haritalama = {}
    config_sutunlar = {
        "SIRA": st.column_config.NumberColumn(disabled=True, width="small"), 
        "ADI SOYADI": st.column_config.TextColumn(disabled=True, width="medium")
    }
    
    for c in st.session_state.calisanlar:
        satir = {"SIRA": int(c["id"]), "ADI SOYADI": str(c["ad_soyad"])}
        for gun in range(1, gun_sayisi + 1):
            try: wd = datetime(secilen_yil, ay_no, gun).weekday()
            except: wd = 0
            s_adi = f"{gun} {gun_kisa_adlar[wd]}"
            sutun_haritalama[gun] = s_adi
            config_sutunlar[s_adi] = st.column_config.TextColumn(width="small")
            
            m_key = f"{secilen_yil}_{ay_no}_{c['id']}_{gun}"
            if m_key not in st.session_state.aylik_matris: 
                st.session_state.aylik_matris[m_key] = ""
            satir[s_adi] = st.session_state.aylik_matris[m_key]
        matris_data.append(satir)
        
    if matris_data:
        st.subheader("🗓️ Günlük Puantaj Girdi Alanı")
        df_matris = pd.DataFrame(matris_data)
        g_tablo = st.data_editor(df_matris, hide_index=True, column_config=config_sutunlar, use_container_width=True, key="m_ed_v_f")
        
        if st.button("💾 Bu Ayın Puantaj Değişikliklerini Veri Tabanına Kaydet"):
            for _, row in g_tablo.iterrows():
                c_id = int(row["SIRA"])
                for gun in range(1, gun_sayisi + 1):
                    s_adi = sutun_haritalama[gun]
                    deger = str(row[s_adi]).strip().upper()
                    if deger not in gecerli_kodlar:
                        deger = ""
                    m_key = f"{secilen_yil}_{ay_no}_{c_id}_{gun}"
                    st.session_state.aylik_matris[m_key] = deger
            verileri_kaydet()
            st.success("✔️ Puantaj veritabanı başarıyla güncellendi!")
            st.rerun()
        
        # --- MAAŞ HESAPLAMA VE RAPORLAMA KISMI (ELIF KOŞULUNUN İÇİNDE) ---
        st.write("---")
        st.markdown(f'<div class="excel-title">💰 {secilen_ay.upper()} {secilen_yil} HAK EDİŞ VE ÖDEME DAĞILIM LİSTESİ</div>', unsafe_allow_html=True)
        
        rapor_verileri = []
        for c in st.session_state.calisanlar:
