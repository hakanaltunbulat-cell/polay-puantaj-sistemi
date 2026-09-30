import streamlit as st
import pandas as pd
from datetime import datetime

# Sayfa Genişlik Ayarı ve Başlık
st.set_page_config(page_title="Puantaj Sistemi", layout="wide", initial_sidebar_state="expanded")

# CSS ile Şık Tasarım Dokunuşları
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .metric-card {
        background-color: white; padding: 20px; border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-left: 5px solid #2563eb;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Şirket Puantaj ve Hak Ediş Otomasyonu")

# 1. VERİ TABANI SİMÜLASYONU (Hafızada Tutma)
if 'calisanlar' not in st.session_state:
    st.session_state.calisanlar = [
        {"id": 1, "ad_soyad": "Ahmet Yılmaz", "tur": "Yevmiye", "ucret": 1200, "giris_tarihi": "2026-10-01", "aktif": True},
        {"id": 2, "ad_soyad": "Mehmet Demir", "tur": "Aylık", "ucret": 35000, "giris_tarihi": "2026-10-10", "aktif": True}
    ]
if 'puantaj' not in st.session_state:
    st.session_state.puantaj = {}

# 2. SOL MENÜ (NAVİGASYON)
st.sidebar.markdown("### 🏢 POLAY PUANTAJ")
st.sidebar.header("👑 Yönetici Paneli")
menu = st.sidebar.radio("Sayfalar", ["📅 Puantaj Girişi", "👤 Çalışan Yönetimi", "💰 Maaş & Ödeme Raporu"])

# --- SAYFA 1: ÇALIŞAN YÖNETİMİ ---
if menu == "👤 Çalışan Yönetimi":
    st.subheader("Yeni Çalışan Ekle / Düzenle")
    
    with st.form("yeni_calisan", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            ad = st.text_input("Adı Soyadı")
            tur = st.selectbox("Maaş Tipi", ["Yevmiye", "Aylık"])
        with col2:
            ucret = st.number_input("Ücret Tutarı (Günlük/Aylık)", min_value=0, value=1000)
            giris_tar = st.date_input("İşe Giriş Tarihi", datetime.now())
            
        submit = st.form_submit_button("💾 Çalışanı Sisteme Kaydet")
        
        if submit and ad:
            yeni_id = len(st.session_state.calisanlar) + 1
            st.session_state.calisanlar.append({
                "id": yeni_id, "ad_soyad": ad, "tur": tur, 
                "ucret": ucret, "giris_tarihi": giris_tar.strftime('%Y-%m-%d'), "aktif": True
            })
            st.success(f"✔️ {ad} başarıyla eklendi!")

    st.write("### 👥 Mevcut Çalışan Listesi")
    df_calisanlar = pd.DataFrame(st.session_state.calisanlar)
    if not df_calisanlar.empty:
        st.dataframe(df_calisanlar[["id", "ad_soyad", "tur", "ucret", "giris_tarihi", "aktif"]], use_container_width=True)

# --- SAYFA 2: PUANTAJ GİRİŞİ ---
elif menu == "📅 Puantaj Girişi":
    st.subheader("Günlük Puantaj Giriş Matrisi")
    secilen_tarih = st.date_input("Puantaj Tarihi Seçin", datetime.now())
    tarih_str = secilen_tarih.strftime('%Y-%m-%d')
    
    st.info("💡 Kodlar: 1 (Çalıştı), 0 (Gelmedi), 2 (Çift Vardiya), Ç (Çıkış)")
    
    # Form Düzeni
    with st.form("puantaj_form"):
        for c in st.session_state.calisanlar:
            if c["aktif"]:
                giris_tarihi_obj = datetime.strptime(c["giris_tarihi"], '%Y-%m-%d').date()
                key = f"{tarih_str}_{c['id']}"
                
                # KURAL: Giriş tarihinden öncesi kilitlenir hesaplanmaz
                if secilen_tarih < giris_tarihi_obj:
                    st.text(f"🔒 {c['ad_soyad']} (Bu tarihte henüz işe başlamamıştı - Giriş: {c['giris_tarihi']})")
                else:
                    mevcut_kod = st.session_state.puantaj.get(key, "1")
                    st.selectbox(f"👤 {c['ad_soyad']} ({c['tur']})", ["1", "0", "2", "Ç"], index=["1", "0", "2", "Ç"].index(mevcut_kod), key=key)
                    
        kaydet = st.form_submit_button("🔒 Günlük Puantajı Onayla ve Kaydet")
        if kaydet:
            for c in st.session_state.calisanlar:
                key = f"{tarih_str}_{c['id']}"
                if key in st.session_state:
                    st.session_state.puantaj[key] = st.session_state[key]
            st.success(f"📊 {tarih_str} tarihli puantaj başarıyla güncellendi!")

# --- SAYFA 3: MAAŞ & ÖDEME RAPORU ---
elif menu == "💰 Maaş & Ödeme Raporu":
    st.subheader("Hak Ediş ve Ödeme Dağılım Listesi")
    
    banka_girdisi = st.number_input("İşçi Başına Bankaya Yatırılacak Sabit Tutar", value=15000, step=1000)
    
    rapor_verisi = []
    
    for c in st.session_state.calisanlar:
        toplam_yevmiye = 0
        giris_tarihi_obj = datetime.strptime(c["giris_tarihi"], '%Y-%m-%d').date()
        is_cikis_yapti = False
        
        # Puantajları tarihe göre sıralayıp tara
        sirali_puantajlar = sorted(st.session_state.puantaj.items())
        
        for k, v in sirali_puantajlar:
            if k.endswith(f"_{c['id']}"):
                p_tarih_str = k.split("_")[0]
                p_tarih_obj = datetime.strptime(p_tarih_str, '%Y-%m-%d').date()
                
                # Yeni Başlayan Kuralı Kontrolü
                if p_tarih_obj < giris_tarihi_obj:
                    continue
                
                # İşten Çıkış Kontrolü
                if is_cikis_yapti:
                    continue
                if v == "Ç":
                    is_cikis_yapti = True
                    continue # Çıktığı gün ve sonrası hesaplanmaz
                
                # Yevmiye Ekleme
                if v == "1": toplam_yevmiye += 1
                elif v == "2": toplam_yevmiye += 2

        # Hak Ediş Hesaplama Kısmı
        if c["tur"] == "Yevmiye":
            hak_edis = toplam_yevmiye * c["ucret"]
        else:
            hak_edis = c["ucret"] # Aylık çalışan sabit alır (Çıkış durumu harici)
            if is_cikis_yapti:
                hak_edis = c["ucret"] / 2 # Basit kıst maaş örneği
                
        banka = min(float(banka_girdisi), float(hak_edis))
        elden = hak_edis - banka
        
        rapor_verisi.append({
            "İşçi Adı": c["ad_soyad"],
            "Tür": c["tur"],
            "İşe Giriş": c["giris_tarihi"],
            "Toplam Hak Ediş": f"{hak_edis:,.2f} ₺",
            "Bankaya Yatacak": f"{banka:,.2f} ₺",
            "Elden Verilecek": f"{elden:,.2f} ₺"
        })
        
    st.table(pd.DataFrame(rapor_verisi))
