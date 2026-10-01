import streamlit as st
import pandas as pd
from datetime import datetime
import sqlite3

# Masaüstü uygulaması görünümü için geniş ekran ayarı
st.set_page_config(page_title="Polay Madencilik Yönetim Sistemi", layout="wide")

KULLANICI_ADI, SIFRE = "polay", "1234"

# ==========================================
# 🗄️ SQLITE VERİ TABANI YÖNETİMİ
# ==========================================
def veritabani_hazirla():
    conn = sqlite3.connect("puantaj.db")
    cursor = conn.cursor()
    
    # 1. Çalışanlar tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calisanlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_soyad TEXT NOT NULL,
            tur TEXT NOT NULL,
            ucret REAL NOT NULL,
            banka_tutari REAL NOT NULL
        )
    """)
    
    # 2. Puantaj matrisi tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS puantaj (
            matris_anahtar TEXT PRIMARY KEY,
            deger TEXT
        )
    """)
    
    # 3. Günlük Üretim ve Faaliyet Tablosu (Yeni Eklenen Bölüm)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gunluk_faaliyet (
            tarih_anahtar TEXT PRIMARY KEY,
            traktor_cevher REAL DEFAULT 0,
            traktor_pasa REAL DEFAULT 0,
            karasik_cevher_pasa REAL DEFAULT 0,
            tahkimat_sayisi INTEGER DEFAULT 0,
            patlayici_delik_sayisi INTEGER DEFAULT 0
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

def gunluk_faaliyet_getir(tarih_str):
    conn = sqlite3.connect("puantaj.db")
    cursor = conn.cursor()
    cursor.execute("SELECT traktor_cevher, traktor_pasa, karasik_cevher_pasa, tahkimat_sayisi, patlayici_delik_sayisi FROM gunluk_faaliyet WHERE tarih_anahtar = ?", (tarih_str,))
    sonuc = cursor.fetchone()
    conn.close()
    if sonuc:
        return sonuc
    return (0.0, 0.0, 0.0, 0, 0)

# Oturum Durumu Kontrolü
if 'giris_yapildi' not in st.session_state: 
    st.session_state.giris_yapildi = False

# 🔒 GÜVENLİ GİRİŞ EKRANI
if not st.session_state.giris_yapildi:
    st.subheader("🔒 POLAY MASAÜSTÜ PUANTAJ & ÜRETİM SİSTEMİ")
    g_kullanici = st.text_input("Yönetici Kullanıcı Adı:")
    g_sifre = st.text_input("Giriş Şifresi:", type="password")
    if st.button("🔓 Sistemde Oturum Aç"):
        if g_kullanici == KULLANICI_ADI and g_sifre == SIFRE:
            st.session_state.giris_yapildi = True
            st.success("Giriş Başarılı!")
            st.rerun()
        else: 
            st.error("🚨 Hatalı Giriş Bilgileri!")
    st.stop()

# 🎨 TASARIM STİLLERİ
st.markdown("""<style>
    .excel-title { background-color: #1e3d59 !important; color: white !important; text-align: center; font-weight: bold; font-size: 22px; padding: 15px; border-radius: 5px; margin-bottom: 15px; }
</style>""", unsafe_allow_html=True)

st.markdown('<div class="excel-title">POLAY MADENCİLİK MASAÜSTÜ YÖNETİM PANELİ</div>', unsafe_allow_html=True)

# 🏢 SOL MENÜ YÖNETİMİ
st.sidebar.markdown("### 🏢 PROGRAM MODÜLLERİ")
islem = st.sidebar.radio("Görüntülenecek Ekran:", [
    "📅 Puantaj Matrisi & Maaş Hakediş", 
    "🚜 Günlük Faaliyet & Üretim Girişi",
    "👤 Çalışan Yönetimi Kartları"
])

if st.sidebar.button("🔒 Programı Güvenli Kapat/Çıkış"): 
    st.session_state.giris_yapildi = False
    st.rerun()

gun_kisa_adlar = {0: "PZT", 1: "SAL", 2: "ÇAR", 3: "PER", 4: "CUM", 5: "CMT", 6: "PZ"}
gecerli_kodlar = ["1", "0", "2", "Ç", ""]
secilen_yil, secilen_ay, ay_no, gun_sayisi = 2026, "Eylül", 9, 30

calisanlar_listesi = calisanlari_getir()
aylik_matris_depo = puantaj_matrisi_getir()

# ==========================================
# 🚜 GÜNLÜK FAALİYET & ÜRETİM GİRİŞİ MODÜLÜ
# ==========================================
if islem == "🚜 Günlük Faaliyet & Üretim Girişi":
    st.subheader("🚜 Günlük İşlenen Faaliyetler ve Cevher/Pasa Takibi")
    
    secilen_gun = st.date_input("İşlem Yapılacak Günü Seçin:", datetime(2026, 9, 1))
    tarih_key = secilen_gun.strftime("%Y_%m_%d")
    
    # Mevcut veriyi çek
    v_cevher, v_pasa, v_karisik, v_tahkimat, v_delik = gunluk_faaliyet_getir(tarih_key)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🪵 Malzeme Taşımacılığı")
        f_cevher = st.number_input("Günlük Gelen Traktör Cevher (Adet/Ton):", min_value=0.0, value=v_cevher, step=1.0)
        f_pasa = st.number_input("Günlük Gelen Traktör Pasa (Adet/Ton):", min_value=0.0, value=v_pasa, step=1.0)
        f_karisik = st.number_input("Günlük Gelen Karışık Traktör Cevher-Pasa (Adet/Ton):", min_value=0.0, value=v_karisik, step=1.0)
        
    with col2:
        st.markdown("### 💣 Üretim & Destek Faaliyeti")
        f_tahkimat = st.number_input("Günlük Atılan Tahkimat Sayısı:", min_value=0, value=v_tahkimat, step=1)
        f_delik = st.number_input("Günlük Kullanılan Patlayıcı Delik Sayısı:", min_value=0, value=v_delik, step=1)

    if st.button("💾 Günlük Faaliyet Verilerini Veritabanına Sabitle"):
        conn = sqlite3.connect("puantaj.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO gunluk_faaliyet 
            (tarih_anahtar, traktor_cevher, traktor_pasa, karasik_cevher_pasa, tahkimat_sayisi, patlayici_delik_sayisi) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (tarih_key, f_cevher, f_pasa, f_karisik, f_tahkimat, f_delik))
        conn.commit()
        conn.close()
        st.success(f"✔️ {secilen_gun.strftime('%d-%m-%Y')} tarihine ait üretim verileri başarıyla kaydedildi!")

    st.write("---")
    st.markdown("### 📊 Bu Ayın Toplam Üretim Grafiği/Tablosu")
    conn = sqlite3.connect("puantaj.db")
    df_tum_faaliyet = pd.read_sql_query("SELECT * FROM gunluk_faaliyet", conn)
    conn.close()
    if not df_tum_faaliyet.empty:
        st.dataframe(df_tum_faaliyet, use_container_width=True, hide_index=True)
    else:
        st.info("Henüz geçmiş günlere ait bir faaliyet kaydı bulunamadı.")

# ==========================================
# 📅 PUANTAJ MATRİSİ & MAAŞ HAKEDİŞ MODÜLÜ
# ==========================================
elif islem == "📅 Puantaj Matrisi & Rapor":
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧨 Ateşçi Ödeneği Ayarları")
    aktif_isimler = [c["ad_soyad"] for c in calisanlar_listesi]
    secilen_atesci = st.sidebar.selectbox("Bu Ayki Ateşçi Kim?", ["Hiçbiri"] + aktif_isimler, index=0)
    atesci_ucreti = st.sidebar.number_input("Ateşçi Ödenek Tutarı (₺)", min_value=0, value=30000, step=5000)
    
    matris_data = []
    sutun_haritalama = {}
    config_sutunlar = {
        "SIRA": st.column_config.NumberColumn(disabled=True), 
        "ADI SOYADI": st.column_config.TextColumn(disabled=True)
    }
    
    for gun in range(1, gun_sayisi + 1):
        try: 
            wd = datetime(secilen_yil, ay_no, gun).weekday()
        except: 
            wd = 0
        s_adi = f"{gun} {gun_kisa_adlar[wd]}"
        sutun_haritalama[gun] = s_adi
        config_sutunlar[s_adi] = st.column_config.SelectboxColumn(options=gecerli_kodlar, width="small")

    for i, c in enumerate(calisanlar_listesi, 1):
        row_dict = {"SIRA": i, "ADI SOYADI": c["ad_soyad"]}
        for gun in range(1, gun_sayisi + 1):
            s_adi = sutun_haritalama[gun]
            anahtar = f"2026_9_{c['id']}_{gun}"
            row_dict[s_adi] = aylik_matris_depo.get(anahtar, "1")
        matris_data.append(row_dict)

    df_matris = pd.DataFrame(matris_data)
    
    st.subheader("📅 Aylık Puantaj Düzenleme Tablosu")
    
    edited_df = st.data_editor(
        df_matris, 
        column_config=config_sutunlar, 
        use_container_width=True, 
        hide_index=True
    )

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
