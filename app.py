import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Puantaj Sistemi", layout="wide", initial_sidebar_state="expanded")
st.title("📊 Şirket Puantaj ve Hak Ediş Otomasyonu")

# 1. GÜNCEL ÇALIŞAN LİSTESİ
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
if 'puantaj' not in st.session_state:
    st.session_state.puantaj = {}

# 2. SOL MENÜ
st.sidebar.markdown("### 🏢 POLAY PUANTAJ")
menu = st.sidebar.radio("Sayfalar", ["📅 Puantaj Girişi", "👤 Çalışan Yönetimi", "💰 Maaş & Ödeme Raporu"])

# --- SAYFA 1: ÇALIŞAN YÖNETİMİ ---
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
            st.session_state.calisanlar.append({
                "id": yeni_id, "ad_soyad": ad, "tur": tur, "ucret": ucret, 
                "banka_tutari": banka_tutari, "giris_tarihi": giris_tar.strftime('%Y-%m-%d'), "aktif": True
            })
            st.success(f"✔️ {ad} başarıyla listeye eklendi!")

    # 🛠️ --- ÇALIŞAN BİLGİLERİNİ DÜZENLEME ALANI ---
    st.write("---")
    st.subheader("✏️ Çalışan Bilgilerini Düzenle / Güncelle")
    aktif_isimler_duzenle = [c["ad_soyad"] for c in st.session_state.calisanlar if c["aktif"]]
    
    if aktif_isimler_duzenle:
        secilen_duzenle = st.selectbox("Bilgilerini değiştirmek istediğiniz çalışanı seçin:", aktif_isimler_duzenle, key="duzenle_sec")
        calisan_bilgi = next(c for c in st.session_state.calisanlar if c["ad_soyad"] == secilen_duzenle)
        
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
                calisan_bilgi["tur"] = yeni_tur
                calisan_bilgi["ucret"] = yeni_ucret
                calisan_bilgi["banka_tutari"] = yeni_banka
                calisan_bilgi["giris_tarihi"] = yeni_giris.strftime('%Y-%m-%d')
                st.success(f"✔️ {secilen_duzenle} isimli çalışanın bilgileri başarıyla güncellendi!")
                st.rerun()

    st.write("---")
    st.write("### 👥 Mevcut Çalışan Listesi")
    df_calisanlar = pd.DataFrame(st.session_state.calisanlar)
    if not df_calisanlar.empty:
        st.dataframe(df_calisanlar[df_calisanlar["aktif"] == True][["id", "ad_soyad", "tur", "ucret", "banka_tutari", "giris_tarihi"]], use_container_width=True)

    # --- İŞÇİ KALICI SİLME ---
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

# --- SAYFA 2: PUANTAJ GİRİŞİ ---
elif menu == "📅 Puantaj Girişi":
    st.subheader("Günlük Puantaj Giriş Matrisi")
    secilen_tarih = st.date_input("Puantaj Tarihi Seçin", datetime.now())
    tarih_str = secilen_tarih.strftime('%Y-%m-%d')
    
    st.info("💡 Kodlar: 1 (Çalıştı), 0 (Gelmedi), 2 (Çift Vardiya), Ç (Çıkış)")
    
    with st.form("puantaj_form"):
        any_active = False
        for c in st.session_state.calisanlar:
            if c["aktif"]:
                any_active = True
                giris_tarihi_obj = datetime.strptime(c["giris_tarihi"], '%Y-%m-%d').date()
                key = f"{tarih_str}_{c['id']}"
                
                if secilen_tarih < giris_tarihi_obj:
                    st.text(f"🔒 {c['ad_soyad']} (Bu tarihte henüz işe başlamamıştı - Giriş: {c['giris_tarihi']})")
                else:
                    mevcut_kod = st.session_state.puantaj.get(key, "1")
                    st.selectbox(f"👤 {c['ad_soyad']} ({c['tur']})", ["1", "0", "2", "Ç"], index=["1", "0", "2", "Ç"].index(mevcut_kod), key=key)
                    
        if any_active:
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
    
    rapor_verisi = []
    
    for c in st.session_state.calisanlar:
        toplam_yevmiye = 0
        giris_tarihi_obj = datetime.strptime(c["giris_tarihi"], '%Y-%m-%d').date()
        is_cikis_yapti = False
        
        haftalik_calisma = {}
        pazar_gunleri = []
        
        sirali_puantajlar = sorted(st.session_state.puantaj.items())
        
        for k, v in sirali_puantajlar:
            if k.endswith(f"_{c['id']}"):
                p_tarih_str = k.split("_")[0]
                p_tarih_obj = datetime.strptime(p_tarih_str, '%Y-%m-%d').date()
                
                if p_tarih_obj < giris_tarihi_obj:
                    continue
                if is_cikis_yapti:
                    continue
                if v == "Ç":
                    is_cikis_yapti = True
                    continue
                
                hafta_key = p_tarih_obj.strftime('%Y-W%U')
                if hafta_key not in haftalik_calisma:
                    haftalik_calisma[hafta_key] = 0
                
                if p_tarih_obj.weekday() == 6:
                    pazar_gunleri.append({"tarih": p_tarih_obj, "hafta_key": hafta_key, "kod": v})
                else:
                    if v == "1": 
                        toplam_yevmiye += 1
                        haftalik_calisma[hafta_key] += 1
                    elif v == "2": 
                        toplam_yevmiye += 2
                        haftalik_calisma[hafta_key] += 1

        for pazar in pazar_gunleri:
            if pazar["kod"] in ["1", "2"]:
                if pazar["kod"] == "1": toplam_yevmiye += 1
                elif pazar["kod"] == "2": toplam_yevmiye += 2
            else:
                hafta_ici_gelme = haftalik_calisma.get(pazar["hafta_key"], 0)
                if hafta_ici_gelme >= 4:
                    toplam_yevmiye += 1

        if c["tur"] == "Yevmiye":
            hak_edis = toplam_yevmiye * c["ucret"]
        else:
            hak_edis = c["ucret"]
            if is_cikis_yapti:
                hak_edis = c["ucret"] / 2
                
        iscinin_kendi_bankasi = float(c["banka_tutari"])
        banka = min(iscinin_kendi_bankasi, float(hak_edis))
        elden = hak_edis - banka
        
        rapor_verisi.append({
            "İşçi Adı": c["ad_soyad"],
            "Tür": c["tur"],
            "İşe Giriş": c["giris_tarihi"],
            "Toplam Hak Ediş": f"{hak_edis:,.2f} ₺",
            "Bankaya Yatacak": f"{banka:,.2f} ₺",
            "Elden Verilecek": f"{elden:,.2f} ₺"
        })
        
    if rapor_verisi:
        st.table(pd.DataFrame(rapor_verisi))
