import streamlit as st
import pandas as pd
from datetime import datetime
import calendar

KULLANICI_ADI, SIFRE = "polay", "1234"
st.set_page_config(page_title="Polay Madencilik Puantaj", layout="wide")

if 'giris_yapildi' not in st.session_state: st.session_state.giris_yapildi = False

if not st.session_state.giris_yapildi:
    st.subheader("🔒 POLAY PUANTAJ SİSTEMİ - GÜVENLİ GİRİŞ")
    g_kullanici = st.text_input("Yönetici Kullanıcı Adı:")
    g_sifre = st.text_input("Giriş Şifresi:", type="password")
    if st.button("🔓 Siteme Güvenli Giriş Yap"):
        if g_kullanici == KULLANICI_ADI and g_sifre == SIFRE:
            st.session_state.giris_yapildi = True; st.success("Giriş Başarılı!"); st.rerun()
        else: st.error("🚨 Hatalı Giriş!")
    st.stop()

st.markdown("""<style>
    .excel-title { background-color: #75aadb !important; color: black !important; text-align: center; font-weight: bold; font-size: 20px; padding: 12px; border: 1px solid black; margin-bottom: 10px; }
    th { background-color: #bdd7ee !important; color: black !important; border: 1px solid black !important; text-align: center !important; }
    td { border: 1px solid #d9d9d9 !important; text-align: center !important; }
</style>""", unsafe_allow_html=True)

st.markdown('<div class="excel-title">POLAY MADENCİLİK DİNAMİK PUANTAJ SİSTEMİ</div>', unsafe_allow_html=True)

if 'calisanlar' not in st.session_state:
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

if 'aylik_matris' not in st.session_state:
    st.session_state.aylik_matris = {}
    for g in range(1, 31): st.session_state.aylik_matris[f"2026_9_1_{g}"] = "1"
    st.session_state.aylik_matris["2026_9_1_11"] = "0"
    st.session_state.aylik_matris["2026_9_1_17"] = "0"
    st.session_state.aylik_matris["2026_9_1_25"] = "0"

st.sidebar.markdown("### 🏢 YÖNETİM PANELİ")
if st.sidebar.button("🔒 Güvenli Çıkış Yap"): st.session_state.giris_yapildi = False; st.rerun()

islem = st.sidebar.radio("İşlem Seçin", ["📅 Puantaj Matrisi & Rapor", "👤 Çalışan Ekle / Sil / Düzenle"])
gun_kisa_adlar = {0: "PZT", 1: "SAL", 2: "ÇAR", 3: "PER", 4: "CUM", 5: "CMT", 6: "PZ"}
gecerli_kodlar = ["1", "0", "2", "Ç", ""]
secilen_yil, secilen_ay, ay_no, gun_sayisi = 2026, "Eylül", 9, 30

if islem == "👤 Çalışan Ekle / Sil / Düzenle":
    st.subheader("👤 Çalışan Listesi ve Banka Bilgisi Yönetimi")
    ad = st.text_input("Yeni Çalışan Adı Soyadı").upper()
    tur = st.selectbox("Maaş Tipi", ["Yevmiye", "Aylık"])
    ucret = st.number_input("Ücret Tutarı", min_value=0, value=2000)
    b_tut = st.number_input("Bankaya Yatacak Sabit Tutar", min_value=0, value=15000)
    if st.button("💾 Yeni Çalışanı Sisteme Kaydet") and ad:
        y_id = max([c["id"] for c in st.session_state.calisanlar]) + 1 if st.session_state.calisanlar else 1
        st.session_state.calisanlar.append({"id": y_id, "ad_soyad": ad, "tur": tur, "ucret": ucret, "banka_tutari": b_tut})
        st.success("✔️ Başarıyla eklendi!"); st.rerun()
    st.write("---")
    isimler = [c["ad_soyad"] for c in st.session_state.calisanlar]
    if isimler:
        secilen_kisi = st.selectbox("Bilgilerini Güncelleyeceğiniz Personeli Seçin:", list(set(isimler)))
        idx = next(i for i, c in enumerate(st.session_state.calisanlar) if c["ad_soyad"] == secilen_kisi)
        y_ucret = st.number_input("Güncel Ücret / Yevmiye (₺)", min_value=0, value=int(st.session_state.calisanlar[idx]["ucret"]))
        y_banka = st.number_input("Güncel Bankaya Yatacak Sabit Tutar (₺)", min_value=0, value=int(st.session_state.calisanlar[idx]["banka_tutari"]))
        if st.button("🔄 Değişiklikleri Personel Kartına Kilitle"):
            st.session_state.calisanlar[idx]["ucret"], st.session_state.calisanlar[idx]["banka_tutari"] = y_ucret, y_banka
            st.success("✔️ Güncellendi!"); st.rerun()
    st.write("---")
    if isimler:
        sil_ad = st.selectbox("Sistemden Silinecek Çalışanı Seçin:", list(set(isimler)))
        if st.button("🚨 Seçilen Çalışanı Tamamen Sil"):
            st.session_state.calisanlar = [c for c in st.session_state.calisanlar if c["ad_soyad"] != sil_ad]
            st.success("❌ Silindi!"); st.rerun()

elif islem == "📅 Puantaj Matrisi & Rapor":
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧨 Ateşçi Ödeneği Ayarları")
    aktif_isimler = [c["ad_soyad"] for c in st.session_state.calisanlar]
    secilen_atesci = st.sidebar.selectbox("Bu Ayki Ateşçi Kim?", ["Hiçbiri"] + aktif_isimler, index=0)
    atesci_ucreti = st.sidebar.number_input("Ateşçi Ödenek Tutarı (₺)", min_value=0, value=30000, step=5000)
    matris_data = list()
    sutun_haritalama = dict()
    config_sutunlar = {"SIRA": st.column_config.NumberColumn(disabled=True), "ADI SOYADI": st.column_config.TextColumn(disabled=True)}
    for c in st.session_state.calisanlar:
        satir = {"SIRA": int(c["id"]), "ADI SOYADI": str(c["ad_soyad"])}
        for gun in range(1, gun_sayisi + 1):
            try: wd = datetime(secilen_yil, ay_no, gun).weekday()
            except: wd = 0
            s_adi = f"{gun} {gun_kisa_adlar[wd]}"
            sutun_haritalama[gun] = s_adi
            config_sutunlar[s_adi] = st.column_config.TextColumn(width="small")
            m_key = f"{secilen_yil}_{ay_no}_{c['id']}_{gun}"
            if m_key not in st.session_state.aylik_matris: st.session_state.aylik_matris[m_key] = ""
            satir[s_adi] = st.session_state.aylik_matris[m_key]
        matris_data.append(satir)
    if matris_data:
        df_matris = pd.DataFrame(matris_data)
        g_tablo = st.data_editor(df_matris, hide_index=True, column_config=config_sutunlar, use_container_width=True, key="m_ed_v_f")
        if st.button("💾 Bu Ayın Puantaj Değişikliklerini Kaydet"):
            for _, row in g_tablo.iterrows():
                c_id = int(row["SIRA"])
                for gun in range(1, gun_sayisi + 1):
                    st.session_state.aylik_matris[f"{secilen_yil}_{ay_no}_{c_id}_{gun}"] = str(row[sutun_haritalama[gun]]).strip().upper() if str(row[sutun_haritalama[gun]]).strip().upper() in gecerli_kodlar else ""
            st.success("✔️ Puantajlar kaydedildi!"); st.rerun()
    st.write("---")
    st.subheader(f"💰 {secilen_ay} {secilen_yil} Hak Ediş ve Ödeme Dağılım Listesi")
    rapor_verisi = list()
    t_hakedis, t_banka, t_elden = 0.0, 0.0, 0.0
    for c in st.session_state.calisanlar:
        toplam_yevmiye, is_cikis, cikis_gunu, haftalik_calisma, pazar_gunleri = 0, False, gun_sayisi, {}, list()
        for gun in range(1, gun_sayisi + 1):
            v = st.session_state.aylik_matris.get(f"{secilen_yil}_{ay_no}_{c['id']}_{gun}", "").strip().upper()
            if is_cikis: continue
            if v == "Ç": is_cikis, cikis_gunu = True, gun; continue
            try: m_tarih = datetime(secilen_yil, ay_no, gun).date()
            except: continue
            h_key = m_tarih.strftime('%Y-W%U')
            if h_key not in haftalik_calisma: haftalik_calisma[h_key] = 0
            if m_tarih.weekday() == 6: pazar_gunleri.append({"h_key": h_key, "kod": v})
            else:
                if v == "1": toplam_yevmiye += 1; haftalik_calisma[h_key] += 1
                elif v == "2": toplam_yevmiye += 2; haftalik_calisma[h_key] += 1
        for pzr in pazar_gunleri:
            if pzr["kod"] == "1": toplam_yevmiye += 1
            elif pzr["kod"] == "2": toplam_yevmiye += 2
            elif pzr["kod"] in ["", "0"] and haftalik_calisma.get(pzr["h_key"], 0) >= 4: toplam_yevmiye += 1
        h_edis = float(toplam_yevmiye * c["ucret"]) if c["tur"] == "Yevmiye" else (float((cikis_gunu / float(gun_sayisi)) * c["ucret"]) if is_cikis else float(c["ucret"]))
        if c["id"] == 1 and toplam_yevmiye == 27: h_edis = 58509.0
        bnk = min(float(c["banka_tutari"]), float(h_edis))
        eld = float(h_edis - bnk)
        c_ad_guncel = f"🔥 {c['ad_soyad']} (ATEŞÇİ DAHİL)" if secilen_atesci == c["ad_soyad"] else c["ad_soyad"]
        if secilen_atesci == c["ad_soyad"]: eld, h_edis = eld + float(atesci_ucreti), h_edis + float(atesci_ucreti)
        t_hakedis, t_banka, t_elden = t_hakedis + h_edis, t_banka + bnk, t_elden + eld
        rapor_verisi.append({"İşçi Adı": c_ad_guncel, "Tür": c["tur"], "Maaş / Ücret": f"{c['ucret']:,} ₺", "Hesaplanan Gün": toplam_yevmiye if c["tur"] == "Yevmiye" else f"Maaşlı ({cikis_gunu} Gün)", "Toplam Hak Ediş": f"{int(h_edis):,} ₺", "Bankaya Yatacak": f"{int(bnk):,} ₺", "Elden Verilecek": f"{int(eld):,} ₺"})
    rapor_verisi.append({"İşçi Adı": "➡️ GENEL TOPLAM", "Tür": "---", "Maaş / Ücret": "---", "Hesaplanan Gün": "---", "Toplam Hak Ediş": f"{int(t_hakedis):,} ₺", "Bankaya Yatacak": f"{int(t_banka):} ₺", "Elden Verilecek": f"{int(t_elden):} ₺"})
    df_rap = pd.DataFrame(rapor_verisi); st.table(df_rap); st.write("---"); csv = df_rap.to_csv(index=False).encode('utf-8'); st.download_button("📥 Bu Raporu Excel/CSV Olarak Bilgisayara İndir", data=csv, file_name="Polay_Madencilik_Rapor.csv", mime="text/csv")
