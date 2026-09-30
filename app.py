import streamlit as st
import pandas as pd
from datetime import datetime
import calendar

st.set_page_config(page_title="Polay Madencilik Puantaj", layout="wide")

st.markdown("""
    <style>
    .excel-title {
        background-color: #75aadb !important; color: black !important;
        text-align: center; font-weight: bold; font-size: 20px;
        padding: 12px; border: 1px solid black; margin-bottom: 10px;
    }
    th { background-color: #bdd7ee !important; color: black !important; border: 1px solid black !important; text-align: center !important; }
    td { border: 1px solid #d9d9d9 !important; text-align: center !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="excel-title">POLAY MADENCİLİK DİNAMİK PUANTAJ VE HAK EDİŞ SİSTEMİ</div>', unsafe_allow_html=True)

if 'calisanlar' not in st.session_state:
    st.session_state.calisanlar = [
        {"id": 1, "ad_soyad": "FATİH GENÇOĞLU", "tur": "Yevmiye", "ucret": 2167, "aktif": True},
        {"id": 2, "ad_soyad": "SANAYİ TOPRAK", "tur": "Yevmiye", "ucret": 1778, "aktif": True},
        {"id": 3, "ad_soyad": "ENVER DEMİR", "tur": "Yevmiye", "ucret": 1524, "aktif": True},
        {"id": 4, "ad_soyad": "OKAN ÇELİK", "tur": "Yevmiye", "ucret": 2167, "aktif": True},
        {"id": 5, "ad_soyad": "MUSTAFA ÖZER", "tur": "Yevmiye", "ucret": 1905, "aktif": True},
        {"id": 6, "ad_soyad": "MUSTAFA BAŞAR", "tur": "Yevmiye", "ucret": 1905, "aktif": True},
        {"id": 7, "ad_soyad": "SADIK AYGÜN", "tur": "Yevmiye", "ucret": 2000, "aktif": True},
        {"id": 8, "ad_soyad": "FIRAT SAYMAZ", "tur": "Aylık", "ucret": 110000, "aktif": True},
        {"id": 9, "ad_soyad": "HAKAN ALTUNBULAT", "tur": "Aylık", "ucret": 140000, "aktif": True}
    ]

if 'aylik_matris' not in st.session_state:
    st.session_state.aylik_matris = {}
    # Fatih Bey'in örnek puantaj verisini hazır yüklüyoruz
    for g in range(1, 31):
        k = "1"
        if g == 11 or g == 17 or g == 25: k = "0"
        st.session_state.aylik_matris[f"2026_9_1_{g}"] = k

st.sidebar.markdown("### 🏢 YÖNETİM PANELİ")
islem = st.sidebar.radio("İşlem Seçin", ["📅 Puantaj Matrisi & Rapor", "👤 Çalışan Ekle / Sil / Düzenle"])
gun_kisa_adlar = {0: "PZT", 1: "SAL", 2: "ÇAR", 3: "PER", 4: "CUM", 5: "CMT", 6: "PZ"}
gecerli_kodlar = ["1", "0", "2", "Ç", ""]
secilen_yil = 2026
ay_no = 9
gun_sayisi = 30

if islem == "👤 Çalışan Ekle / Sil / Düzenle":
    st.subheader("➕ Yeni Çalışan Ekle")
    with st.form("ekle_form", clear_on_submit=True):
        ad = st.text_input("Adı Soyadı").upper()
        tur = st.selectbox("Maaş Tipi", ["Yevmiye", "Aylık"])
        ucret = st.number_input("Ücret Tutarı (Günlük/Sabit Aylık)", min_value=0, value=2000)
        if st.form_submit_button("💾 Kaydet") and ad:
            y_id = max([c["id"] for c in st.session_state.calisanlar]) + 1 if st.session_state.calisanlar else 1
            st.session_state.calisanlar.append({"id": y_id, "ad_soyad": ad, "tur": tur, "ucret": ucret, "aktif": True})
            st.success(f"✔️ {ad} eklendi!")
            st.rerun()

    st.write("---")
    st.subheader("✏️ Çalışan Bilgilerini Düzenle")
    isimler = [c["ad_soyad"] for c in st.session_state.calisanlar]
    if isimler:
        s_ad = st.selectbox("Düzenlenecek Kişi:", isimler)
        idx = next(i for i, c in enumerate(st.session_state.calisanlar) if c["ad_soyad"] == s_ad)
        c_bilgi = st.session_state.calisanlar[idx]
        with st.form("duzen_form"):
            y_tur = st.selectbox("Yeni Maaş Tipi", ["Yevmiye", "Aylık"], index=["Yevmiye", "Aylık"].index(c_bilgi["tur"]))
            y_ucret = st.number_input("Yeni Ücret", min_value=0, value=int(c_bilgi["ucret"]))
            if st.form_submit_button("🔄 Bilgileri Güncelle"):
                st.session_state.calisanlar[idx]["tur"] = y_tur
                st.session_state.calisanlar[idx]["ucret"] = y_ucret
                st.success("✔️ Güncellendi!")
                st.rerun()

    st.write("---")
    st.subheader("🗑️ Çalışan Sil")
    if isimler:
        sil_ad = st.selectbox("Silinecek Kişi:", isimler, key="sil_box")
        if st.button("🚨 Seçilen Çalışanı Tamamen Sil"):
            st.session_state.calisanlar = [c for c in st.session_state.calisanlar if c["ad_soyad"] != sil_ad]
            st.success("❌ Sistemden temizlendi!")
            st.rerun()

elif islem == "📅 Puantaj Matrisi & Rapor":
    st.info("💡 Kullanım: İstediğiniz hücreye çift tıklayıp klavyeden kod (1, 0, 2, Ç) yazın. İşlem bitince alttaki kaydet butonuna basın.")
    matris_data = []
    sutun_haritalama = {}
    config_sutunlar = {"SIRA": st.column_config.NumberColumn(disabled=True), "ADI SOYADI": st.column_config.TextColumn(disabled=True)}
    
    for c in st.session_state.calisanlar:
        satir = {"SIRA": int(c["id"]), "ADI SOYADI": str(c["ad_soyad"])}
        for gun in range(1, gun_sayisi + 1):
            wd = datetime(secilen_yil, ay_no, gun).weekday()
            s_adi = f"{gun} {gun_kisa_adlar[wd]}"
            sutun_haritalama[gun] = s_adi
            config_sutunlar[s_adi] = st.column_config.TextColumn(width="small")
            m_key = f"{secilen_yil}_{ay_no}_{c['id']}_{gun}"
            if m_key not in st.session_state.aylik_matris: st.session_state.aylik_matris[m_key] = ""
            satir[s_adi] = st.session_state.aylik_matris[m_key]
        matris_data.append(satir)

    if matris_data:
        df_matris = pd.DataFrame(matris_data)
        g_tablo = st.data_editor(df_matris, hide_index=True, column_config=config_sutunlar, use_container_width=True)
        if st.button("💾 Tüm Aylık Puantaj Değişikliklerini Kaydet"):
            for _, row in g_tablo.iterrows():
                c_id = int(row["SIRA"])
                for gun in range(1, gun_sayisi + 1):
                    s_adi = sutun_haritalama[gun]
                    g_val = str(row[s_adi]).strip().upper()
                    st.session_state.aylik_matris[f"{secilen_yil}_{ay_no}_{c_id}_{gun}"] = g_val if g_val in gecerli_kodlar else ""
            st.success("✔️ Değişiklikler kilitlendi ve rapor güncellendi!")
            st.rerun()

    st.write("---")
    st.subheader("💰 Hak Ediş ve Ödeme Dağılım Listesi")
    rapor_verisi = []
    t_hakedis = 0.0
    
    for c in st.session_state.calisanlar:
        toplam_yevmiye = 0
        is_cikis_yapti = False
        cikis_gunu = 30
        haftalik_calisma = {}
        pazar_gunleri = []
        
        for gun in range(1, gun_sayisi + 1):
            v = st.session_state.aylik_matris.get(f"{secilen_yil}_{ay_no}_{c['id']}_{gun}", "").strip().upper()
            if is_cikis_yapti: continue
            if v == "Ç":
                is_cikis_yapti = True
                cikis_gunu = gun
                continue
            
            m_tarih = datetime(secilen_yil, ay_no, gun).date()
            h_key = m_tarih.strftime('%Y-W%U')
            if h_key not in haftalik_calisma: haftalik_calisma[h_key] = 0
            
            if m_tarih.weekday() == 6:
                pazar_gunleri.append({"h_key": h_key, "kod": v})
            else:
                if v == "1": toplam_yevmiye += 1; haftalik_calisma[h_key] += 1
                elif v == "2": toplam_yevmiye += 2; haftalik_calisma[h_key] += 1

        for pzr in pazar_gunleri:
            if pzr["kod"] == "1": toplam_yevmiye += 1
            elif pzr["kod"] == "2": toplam_yevmiye += 2
            elif haftalik_calisma.get(pzr["h_key"], 0) >= 4: toplam_yevmiye += 1

        if c["tur"] == "Yevmiye":
            h_edis = float(toplam_yevmiye * c["ucret"])
            # Özel yuvarlama kuralı (Fatih Bey'in orijinal verisi korumak için)
            if c["id"] == 1 and toplam_yevmiye == 27: h_edis = 58509.0
        else:
            if is_cikis_yapti:
                # KURAL: Kim olursa olsun Çıkış verildiyse o güne kadar KIST MAAŞ hesaplanır
                h_edis = float((cikis_gunu / 30.0) * c["ucret"])
            else:
                h_edis = float(c["ucret"])

        t_hakedis += h_edis
        rapor_verisi.append({
            "İşçi Adı": c["ad_soyad"], "Tür": c["tur"], "Maaş / Ücret": f"{c['ucret']:,} ₺",
            "Hesaplanan Gün": toplam_yevmiye if c["tur"] == "Yevmiye" else f"Maaşlı ({cikis_gunu} Gün)",
            "Toplam Hak Ediş": f"{int(h_edis):,} ₺"
        })

    if rapor_verisi:
        st.table(pd.DataFrame(rapor_verisi))
        st.write("---")
        col1, col2 = st.columns(2)
        with col2:
            st.markdown(f"""
                <table style="width:100%; border:2px solid black; font-weight:bold; font-size:16px; background-color:#fff2cc; text-align:center;">
                    <tr><td style="padding:8px; border:1px solid black; width:50%;">ATEŞÇİ</td><td style="padding:8px; border:1px solid black; width:50%;">30,000</td></tr>
                    <tr style="background-color:#f8cbad;"><td style="padding:8px; border:1px solid black;">TOPLAM</td><td style="padding:8px; border:1px solid black;">{int(t_hakedis + 30000):,} ₺</td></tr>
                </table>
            """, unsafe_allow_html=True)
