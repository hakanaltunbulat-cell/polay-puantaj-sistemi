import streamlit as st
import pandas as pd
from datetime import datetime
import sqlite3
import io

KULLANICI_ADI, SIFRE = "polay", "1234"
st.set_page_config(page_title="Polay Madencilik Puantaj", layout="wide")

# ==========================================
# 🗄️ SQLITE VERİ TABANI YÖNETİMİ
# ==========================================
def veritabani_hazirla():
    conn = sqlite3.connect("puantaj.db")
    cursor = conn.cursor()
    # Çalışanlar tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calisanlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_soyad TEXT NOT NULL,
            tur TEXT NOT NULL,
            ucret REAL NOT NULL,
            banka_tutari REAL NOT NULL
        )
    """)
    # Puantaj matrisi tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS puantaj (
            matris_anahtar TEXT PRIMARY KEY,
            deger TEXT
        )
    """)
    conn.commit()
    
    # Eğer tablo tamamen boşsa varsayılan çalışanları yükle
    cursor.execute("SELECT COUNT(*) FROM calisanlar")
    if cursor.fetchone()[0] == 0:
        varsayilan_calisanlar = [
            ("FATİH GENÇOĞLU", "Yevmiye", 2167, 34750),
            ("SANAYİ TOPRAK", "Yevmiye", 1778, 15000),
            ("ENVER DEMİR", "Yevmiye", 1524, 15000),
            ("OKAN ÇELİK", "Yevmiye", 2167, 15000),
            ("MUSTAFA ÖZER", "Yevmiye", 1905, 15000),
            ("MUSTAFA BAŞAR", "Yevmiye", 1905, 15000),
            ("SADIK AYGÜN", "Yevmiye", 2000, 15000),
            ("FIRAT SAYMAZ", "Aylık", 110000, 15000),
            ("HAKAN ALTUNBULAT", "Aylık", 140000, 15000)
        ]
        cursor.executemany("INSERT INTO calisanlar (ad_soyad, tur, ucret, banka_tutari) VALUES (?, ?, ?, ?)", varsayilan_calisanlar)
        conn.commit()
        
        # Varsayılan değerleri matrise işle
        cursor.execute("SELECT id FROM calisanlar")
        isciler = cursor.fetchall()
        for isci in isciler:
            isci_id = isci[0]
            for g in range(1, 31):
                kod = "0" if g in [11, 17, 25] else "1"
                cursor.execute("INSERT OR REPLACE INTO puantaj (matris_anahtar, deger) VALUES (?, ?)", (f"2026_9_{isci_id}_{g}", kod))
        conn.commit()
    conn.close()

# Veritabanı altyapısını başlat
veritabani_hazirla()

def calisanlari_getir():
    conn = sqlite3.connect("puantaj.db")
    df = pd.read_sql_query("SELECT * FROM calisanlar", conn)
    conn.close()
    return df.to_dict(orient="records")

def puantaj_matrisi_getir():
    conn = sqlite3.connect("puantaj.db")
    cursor = conn.cursor()
    cursor.execute("SELECT matris_anahtar, deger FROM puantaj")
    veriler = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in veriler}

# Oturum Durumu Kontrolü
if 'giris_yapildi' not in st.session_state: 
    st.session_state.giris_yapildi = False

# 🔒 GÜVENLİ GİRİŞ EKRANI
if not st.session_state.giris_yapildi:
    st.subheader("🔒 POLAY PUANTAJ SİSTEMİ - GÜVENLİ GİRİŞ")
    g_kullanici = st.text_input("Yönetici Kullanıcı Adı:")
    g_sifre = st.text_input("Giriş Şifresi:", type="password")
    if st.button("🔓 Siteme Güvenli Giriş Yap"):
        if g_kullanici == KULLANICI_ADI and g_sifre == SIFRE:
            st.session_state.giris_yapildi = True
            st.success("Giriş Başarılı!")
            st.rerun()
        else: 
            st.error("🚨 Hatalı Giriş!")
    st.stop()

# 🎨 EXCEL BENZERİ TABLO STİLLERİ
st.markdown("""<style>
    .excel-title { background-color: #75aadb !important; color: black !important; text-align: center; font-weight: bold; font-size: 20px; padding: 12px; border: 1px solid black; margin-bottom: 10px; }
    th { background-color: #bdd7ee !important; color: black !important; border: 1px solid black !important; text-align: center !important; }
    td { border: 1px solid #d9d9d9 !important; text-align: center !important; }
</style>""", unsafe_allow_html=True)

st.markdown('<div class="excel-title">POLAY MADENCİLİK DİNAMİK PUANTAJ SİSTEMİ</div>', unsafe_allow_html=True)

# 🏢 SOL MENÜ YÖNETİMİ
st.sidebar.markdown("### 🏢 YÖNETİM PANELİ")
if st.sidebar.button("🔒 Güvenli Çıkış Yap"): 
    st.session_state.giris_yapildi = False
    st.rerun()

islem = st.sidebar.radio("İşlem Seçin", ["📅 Puantaj Matrisi & Rapor", "👤 Çalışan Ekle / Sil / Düzenle"])
gun_kisa_adlar = {0: "PZT", 1: "SAL", 2: "ÇAR", 3: "PER", 4: "CUM", 5: "CMT", 6: "PZ"}
gecerli_kodlar = ["1", "0", "2", "Ç", ""]
secilen_yil, secilen_ay, ay_no, gun_sayisi = 2026, "Eylül", 9, 30

# Veritabanından güncel bilgileri çek
calisanlar_listesi = calisanlari_getir()
aylik_matris_depo = puantaj_matrisi_getir()

# ==========================================
# 👤 ÇALIŞAN EKLE / SİL / DÜZENLE MODÜLÜ
# ==========================================
if islem == "👤 Çalışan Ekle / Sil / Düzenle":
    st.subheader("👤 Çalışan Listesi ve Banka Bilgisi Yönetimi")
    ad = st.text_input("Yeni Çalışan Adı Soyadı").upper()
    tur = st.selectbox("Maaş Tipi", ["Yevmiye", "Aylık"])
    ucret = st.number_input("Ücret Tutarı", min_value=0, value=2000)
    b_tut = st.number_input("Bankaya Yatacak Sabit Tutar", min_value=0, value=15000)
    
    if st.button("💾 Yeni Çalışanı Sisteme Kaydet") and ad:
        conn = sqlite3.connect("puantaj.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO calisanlar (ad_soyad, tur, ucret, banka_tutari) VALUES (?, ?, ?, ?)", (ad, tur, ucret, b_tut))
        conn.commit()
        conn.close()
        st.success("✔️ Çalışan veritabanına kalıcı olarak kaydedildi!")
        st.rerun()
        
    st.write("---")
    isimler = [c["ad_soyad"] for c in calisanlar_listesi]
    if isimler:
        secilen_kisi = st.selectbox("Bilgilerini Güncelleyeceğiniz Personeli Seçin:", list(set(isimler)))
        idx = next(i for i, c in enumerate(calisanlar_listesi) if c["ad_soyad"] == secilen_kisi)
        
        y_ucret = st.number_input("Güncel Ücret / Yevmiye (₺)", min_value=0, value=int(calisanlar_listesi[idx]["ucret"]))
        y_banka = st.number_input("Güncel Bankaya Yatacak Sabit Tutar (₺)", min_value=0, value=int(calisanlar_listesi[idx]["banka_tutari"]))
        
        if st.button("🔄 Değişiklikleri Personel Kartına Kilitle"):
            conn = sqlite3.connect("puantaj.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE calisanlar SET ucret = ?, banka_tutari = ? WHERE id = ?", (y_ucret, y_banka, calisanlar_listesi[idx]["id"]))
            conn.commit()
            conn.close()
            st.success("✔️ Bilgiler veritabanında güncellendi!")
            st.rerun()
            
    st.write("---")
    if isimler:
        sil_ad = st.selectbox("Sistemden Silinecek Çalışanı Seçin:", list(set(isimler)))
        if st.button("🚨 Seçilen Çalışanı Tamamen Sil"):
            conn = sqlite3.connect("puantaj.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM calisanlar WHERE ad_soyad = ?", (sil_ad,))
            conn.commit()
            conn.close()
            st.success("❌ Çalışan veritabanından kalıcı olarak silindi!")
            st.rerun()

# ==========================================
# 📅 PUANTAJ MATRİSİ & RAPOR MODÜLÜ
# ==========================================
elif islem == "📅 Puantaj Matrisi & Rapor":
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧨 Ateşçi Ödeneği Ayarları")
    aktif_isimler = [c["ad_soyad"] for c in calisanlar_listesi]
    secilen_atesci = st.sidebar.selectbox("Bu Ayki Ateşçi Kim?", ["Hiçbiri"] + aktif_isimler, index=0)
    atesci_ucreti = st.sidebar.number_input("Ateşçi Ödenek Tutarı (₺)", min_value=0, value=30000, step=5000)
    
    matris_data = list()
    sutun_haritalama = dict()
    config_sutunlar = {
        "SIRA": st.column_config.NumberColumn(disabled=True), 
        "ADI SOYADI": st.column_config.TextColumn(disabled=True)
    }
    
    # Gün başlıklarını oluşturma
    for gun in range(1, gun_sayisi + 1):
        try: 
            wd = datetime(secilen_yil, ay_no, gun).weekday()
        except: 
            wd = 0
        s_adi = f"{gun} {gun_kisa_adlar[wd]}"
        sutun_haritalama[gun] = s_adi
        config_sutunlar[s_adi] = st.column_config.SelectboxColumn(options=gecerli_kodlar, width="small")

    # Matris satırlarını veritabanından doldurma
    for i, c in enumerate(calisanlar_listesi, 1):
        row_dict = {"SIRA": i, "ADI SOYADI": c["ad_soyad"]}
        for gun in range(1, gun_sayisi + 1):
            s_adi = sutun_haritalama[gun]
            anahtar = f"2026_9_{c['id']}_{gun}"
            row_dict[s_adi] = aylik_matris_depo.get(anahtar, "1")
        matris_data.append(row_dict)

    df_matris = pd.DataFrame(matris_data)
    
    st.subheader("📅 Aylık Puantaj Düzenleme Tablosu")
    st.info("💡 Tablo üzerinde değişiklik yapabilir, kutucuklardan puantaj kodlarını (1, 0, 2, Ç) seçebilirsiniz.")
    
    # Streamlit veri düzenleyici editörü
    edited_df = st.data_editor(
        df_matris, 
        column_config=config_sutunlar, 
        use_container_width=True, 
        hide_index=True
    )

    # Değişiklikleri Veritabanına Kaydetme Butonu
    if st.button("💾 Puantaj Değişikliklerini Veritabanına Kaydet"):
        conn = sqlite3.connect("puantaj.db")
        cursor = conn.cursor()
        for _, row in edited_df.iterrows():
            ad_soyad = row["ADI SOYADI"]
            c_id = next(c["id"] for c in calisanlar_listesi if c["ad_soyad"] == ad_soyad)
            for gun in range(1, gun_sayisi + 1):
                s_adi = sutun_haritalama[gun]
                yeni_deger = str(row[s_adi]) if row[s_adi] is not None else ""
                anahtar = f"2026_9_{c_id}_{gun}"
                cursor.execute("INSERT OR REPLACE INTO puantaj (matris_anahtar, deger) VALUES (?, ?)", (anahtar, yeni_deger))
        conn.commit()
        conn.close()
        st.success("✔️ Tüm puantaj değişiklikleri veritabanına başarıyla kilitlendi!")
        st.rerun()

    # ==========================================
