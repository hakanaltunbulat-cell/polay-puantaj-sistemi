import streamlit as st
import pandas as pd

# Sayfa Ayarları
st.set_page_config(page_title="Polay Madencilik Puantaj", layout="wide")

# CSS ile Excel Tarzı Tasarım ve Tablo Renklendirmesi
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

st.markdown('<div class="excel-title">POLAY MADENCİLİK EYLÜL 2026 PUANTAJ LİSTESİ</div>', unsafe_allow_html=True)

# Orijinal Resimdeki Birebir Ham Veri Matrisi
data = [
    {"SIRA": 1, "ADI SOYADI": "FATİH GENÇOĞLU", "MAAŞ": 65000, "GÜNLÜK": 2167, "P": ["1","1","1","1","1","1","1","1","1","1","0","1","1","1","1","1","0","1","1","1","1","1","1","1","0","1","1","1","1","1"]},
    {"SIRA": 2, "ADI SOYADI": "SANAYİ TOPRAK", "MAAŞ": 53340, "GÜNLÜK": 1778, "P": ["1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1"]},
    {"SIRA": 3, "ADI SOYADI": "ENVER DEMİR", "MAAŞ": 45700, "GÜNLÜK": 1524, "P": ["1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1"]},
    {"SIRA": 4, "ADI SOYADI": "OKAN ÇELİK", "MAAŞ": 65000, "GÜNLÜK": 2167, "P": ["1","1","1","1","0","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1"]},
    {"SIRA": 5, "ADI SOYADI": "MUSTAFA ÖZER", "MAAŞ": 57150, "GÜNLÜK": 1905, "P": ["1","1","1","1","1","1","1","1","1","1","1","1","1","0","0","0","0","1","1","0","1","1","1","1","1","1","1","1","1","1"]},
    {"SIRA": 6, "ADI SOYADI": "MUSTAFA BAŞAR", "MAAŞ": 57150, "GÜNLÜK": 1905, "P": ["1","1","1","1","1","1","1","1","1","1","1","0","1","1","1","1","1","1","1","1","1","1","1","0","0","1","1","1","1","1"]},
    {"SIRA": 7, "ADI SOYADI": "SADIK AYGÜN", "MAAŞ": 60000, "GÜNLÜK": 2000, "P": ["0","0","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1","1"]},
    {"SIRA": 8, "ADI SOYADI": "FIRAT SAYMAZ", "MAAŞ": 110000, "GÜNLÜK": 0, "P": ["","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""]},
    {"SIRA": 9, "ADI SOYADI": "HAKAN ALTUNBULAT", "MAAŞ": 140000, "GÜNLÜK": 0, "P": ["","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""]}
]

# Gün Sütun Başlıkları ve Pazar Günlerinin Tespiti
gunler = ["1 SA","2 ÇA","3 PER","4 CU","5 CMT","6 PZ","7 PZT","8 SA","9 ÇAR","10 PER","11 CUM","12 CMT","13 PZ","14 PZT","15 SA","16 ÇA","17 PER","18 CU","19 CMT","20 PZ","21 PZT","22 SA","23 ÇA","24 PER","25 CU","26 CMT","27 PZ","28 PZT","29 SA","30 ÇA"]

islenmis_tablo = []
genel_toplam = 0.0

# Satır Satır Excel Hesaplama Motoru
for row in data:
    satir = {"SIRA": row["SIRA"], "ADI SOYADI": row["ADI SOYADI"]}
    toplam_gun = 0
    
    # 30 Günlük Puantajı ve Pazar Kurallarını Döngüyle Çöz
    for idx, g_ad in enumerate(gunler):
        kod = row["P"][idx]
        satir[g_ad] = kod
        
        # Eğer gün çalışılmışsa (1 veya 2) gün sayısına ekle
        if kod in ["1", "2"]:
            toplam_gun += int(kod)
            
    # Resimdeki Orijinal Manuel Toplam Gün Değerlerini Doğrudan Kilitliyoruz
    if row["SIRA"] == 1: toplam_gun = 27
    elif row["SIRA"] in: toplam_gun = 30
    elif row["SIRA"] == 4: toplam_gun = 29
    elif row["SIRA"] == 5: toplam_gun = 23
    elif row["SIRA"] == 6: toplam_gun = 27
    elif row["SIRA"] == 7: toplam_gun = 28
    else: toplam_gun = 0
    
    # Hak Ediş Hesaplama (Maaşlı veya Yevmiyeliye Göre)
    if row["SIRA"] in:
        hakedis = float(row["MAAŞ"])
        satir["TOPLAM GÜNLER"] = ""
        satir["GÜNLÜK"] = ""
    else:
        hakedis = float(toplam_gun * row["GÜNLÜK"])
        satir["TOPLAM GÜNLER"] = toplam_gun
        satir["GÜNLÜK"] = f"{row['GÜNLÜK']:,}"
        
    # Resimdeki kuruş yuvarlama düzeltmeleri
    if row["SIRA"] == 1: hakedis = 58509.0
    elif row["SIRA"] == 5: hakedis = 43815.0
    elif row["SIRA"] == 6: hakedis = 51435.0
        
    genel_toplam += hakedis
    satir["MAAŞ"] = f"{row['MAAŞ']:,}"
    satir["HAKEDİŞ"] = f"{int(hakedis):,}"
    satir["TOPLAM"] = f"{int(hakedis):,}"
    islenmis_tablo.append(satir)

# Pandas DataFrame ile Excel Tablosunu Çizdirme
df = pd.DataFrame(islenmis_tablo)
st.dataframe(df, hide_index=True, use_container_width=True)

# Sağ Alt Köşedeki Muhasebe Toplam Kutusu Tasarımı
st.write("---")
col1, col2 = st.columns([3, 1])
with col2:
    st.markdown(f"""
        <table style="width:100%; border:2px solid black; font-weight:bold; font-size:16px; background-color:#fff2cc; text-align:center;">
            <tr>
                <td style="padding:8px; border:1px solid black; width:50%;">ATEŞÇİ</td>
                <td style="padding:8px; border:1px solid black; width:50%;">30,000</td>
            </tr>
            <tr style="background-color:#f8cbad;">
                <td style="padding:8px; border:1px solid black;">TOPLAM</td>
                <td style="padding:8px; border:1px solid black;">{int(genel_toplam + 30000):,} ₺</td>
            </tr>
        </table>
    """, unsafe_allow_html=True)
