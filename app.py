import streamlit as st
import random
import pandas as pd
import os

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Survivor: Niko'nun 30 Günü", page_icon="🛡️", layout="centered")

# --- CSS ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #1CB5E0 0%, #000851 100%);
        color: white !important;
        font-size: 20px;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 15px;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 7px 20px rgba(0,0,0,0.3);
    }
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 10px;
        padding: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- SKOR KAYDETME ---
DOSYA_ADI = "skorlar_v5_top5.csv" 

def skor_yukle():
    if not os.path.exists(DOSYA_ADI):
        return pd.DataFrame(columns=["İsim", "Can", "XP", "Skor"])
    return pd.read_csv(DOSYA_ADI)

def skor_kaydet(isim, can, xp):
    df = skor_yukle()
    toplam_skor = can + xp
    yeni_kayit = pd.DataFrame({"İsim": [isim], "Can": [can], "XP": [xp], "Skor": [toplam_skor]})
    df = pd.concat([df, yeni_kayit], ignore_index=True)
    df = df.sort_values(by="Skor", ascending=False)
    
    # Teknik olarak hala ilk 5'i tutuyoruz ki liste uzamasın
    df = df.head(5)
    
    df.to_csv(DOSYA_ADI, index=False)

# --- OYUN SABİTLERİ ---
HEDEF_GUN = 30 

# --- BAŞLIK ---
st.title(f"🛡️ Survivor: Niko'nun 30 Günü")
# BURAYI DÜZENLEDİK
st.markdown("**Hedef:** 30 gün boyunca hayatta kal.")

# --- SIDEBAR ---
st.sidebar.header("👤 Oyuncu")
if 'oyuncu_ismi' not in st.session_state: st.session_state.oyuncu_ismi = "Niko"
isim_input = st.sidebar.text_input("İsminiz:", st.session_state.oyuncu_ismi)
st.session_state.oyuncu_ismi = isim_input

zeka = st.sidebar.slider("Zeka (IQ)", 50, 160, 135)

# --- LİDERLİK TABLOSU ---
st.sidebar.divider()
st.sidebar.header("🏆 Liderlik Tablosu")
df_skor = skor_yukle()
if not df_skor.empty:
    st.sidebar.dataframe(df_skor, hide_index=True)
else:
    st.sidebar.info("Liste boş. Zirve seni bekliyor!")

# --- DEĞİŞKENLER ---
if 'ruh_sagligi' not in st.session_state: st.session_state.ruh_sagligi = 100
if 'para' not in st.session_state: st.session_state.para = 1000 
if 'gun_sayaci' not in st.session_state: st.session_state.gun_sayaci = 1
if 'tecrube' not in st.session_state: st.session_state.tecrube = 0 
if 'log' not in st.session_state: st.session_state.log = []
if 'gecmis_can' not in st.session_state: st.session_state.gecmis_can = [100] 
if 'oyun_bitti' not in st.session_state: st.session_state.oyun_bitti = False
if 'kazandi' not in st.session_state: st.session_state.kazandi = False
if 'son_olay' not in st.session_state: st.session_state.son_olay = "Başlangıç..."
if 'son_kategori' not in st.session_state: st.session_state.son_kategori = "siradan"
if 'skor_kaydedildi' not in st.session_state: st.session_state.skor_kaydedildi = False

# --- MARKET ---
st.sidebar.divider()
st.sidebar.header("🛒 Market")
st.sidebar.write(f"💰 Bakiye: **{st.session_state.para} TL**")
col_m1, col_m2 = st.sidebar.columns(2)

# Kahve aynı kaldı
if col_m1.button("☕ Kahve (200)"):
    if st.session_state.para >= 200:
        st.session_state.para -= 200
        st.session_state.ruh_sagligi += 15
        if st.session_state.ruh_sagligi > 100: st.session_state.ruh_sagligi = 100
        st.sidebar.success("Can Yenilendi!")
        st.rerun()

# BURAYI DÜZENLEDİK: KULAKLIK -> KONSER
if col_m2.button("🎫 Konser (500)"):
    if st.session_state.para >= 500:
        st.session_state.para -= 500
        st.session_state.ruh_sagligi += 40
        if st.session_state.ruh_sagligi > 100: st.session_state.ruh_sagligi = 100
        st.sidebar.success("Müziğin ritmine kapıldın! (+40 Can)")
        st.rerun()
    else:
        st.sidebar.error("Bilet için paran yetmiyor!")

# --- DASHBOARD ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("❤️ Sağlık", f"{st.session_state.ruh_sagligi}")
c2.metric("💰 Para", f"{st.session_state.para} TL")
c3.metric("📅 Gün", f"{st.session_state.gun_sayaci}/{HEDEF_GUN}")
c4.metric("✨ XP", st.session_state.tecrube)
st.progress(min(st.session_state.gun_sayaci / HEDEF_GUN, 1.0))
st.divider()

# --- OYUN AKIŞI ---

if not st.session_state.oyun_bitti:
    
    st.subheader(f"🌅 {st.session_state.gun_sayaci}. Gün")
    
    # BURAYI DÜZENLEDİK: BUTON METNİ
    if st.button(f"🎲 Yeni Güne Uyan"):
        
        # --- KATEGORİLENDİRİLMİŞ OLAYLAR ---
        
        # 1. SIRADAN (%60)
        siradan_olaylar = [
            ("Sokakta kedi sevdin", 10, "pozitif", 0),
            ("Kahve döküldü", 5, "negatif", -50),
            ("Otobüsü kaçırdın", 10, "negatif", -20),
            ("Güzel bir şarkı dinledin", 5, "pozitif", 0),
            ("Market alışverişi yaptın", 5, "negatif", -300),
            ("Arkadaşınla sohbet ettin", 10, "pozitif", 0),
            ("İnternet yavaştı", 10, "negatif", 0),
            ("Yemeği fazla kaçırdın", 5, "negatif", -100),
            ("Yerde 10 TL buldun", 5, "pozitif", 10),
            ("Hava çok güzel", 10, "pozitif", 0),
            ("Klimadan boynun tutuldu", 10, "negatif", 0),
            ("Patron 'Günaydın' dedi", 5, "pozitif", 0),
            ("Uykunu iyi aldın", 15, "pozitif", 0),
            ("Trafik vardı", 10, "negatif", -50)
        ]
        
        # 2. NADİR (%30)
        nadir_olaylar = [
            ("Maaş yattı", 10, "pozitif", 5000),
            ("Trafik cezası yedin", 20, "negatif", -1000),
            ("Dişin ağrıdı, dolgu yaptırdın", 25, "negatif", -2000),
            ("Freelance iş geldi", 20, "pozitif", 2000),
            ("Patron fırça attı", 25, "negatif", 0),
            ("Eski arkadaşın borcunu ödedi", 15, "pozitif", 500),
            ("Telefonun camı çatladı", 20, "negatif", -1500),
            ("Küçük bir hediye aldın", 20, "pozitif", 0),
            ("Ayakkabın yırtıldı", 15, "negatif", -1000),
            ("Kodun tek seferde çalıştı", 25, "pozitif", 0)
        ]
        
        # 3. KRİTİK / EFSANE (%10)
        kritik_olaylar = [
            ("DOLANDIRILDIN! Hesabın boşaltıldı", 40, "negatif", -5000),
            ("PİYANGO vurdu! (Şaka değil)", 40, "pozitif", 10000),
            ("İFTİRA atıldı, çok gerildin", 50, "negatif", 0),
            ("BÜYÜK TERFİ aldın!", 50, "pozitif", 5000),
            ("BİLGİSAYAR ÇÖKTÜ, her şey silindi", 45, "negatif", -5000),
            ("MİRAS gibi para geldi", 40, "pozitif", 7500),
            ("HASTANELİK oldun (Acil Durum)", 50, "negatif", -3000)
        ]
        
        # --- ZAR ATMA ---
        secilen_kategori = random.choices(
            ["siradan", "nadir", "kritik"], 
            weights=[60, 30, 10], 
            k=1
        )[0]
        
        if secilen_kategori == "siradan":
            havuz = siradan_olaylar
        elif secilen_kategori == "nadir":
            havuz = nadir_olaylar
        else:
            havuz = kritik_olaylar
            
        olay_adi, etki, tip, para_etkisi = random.choice(havuz)
        
        degisim = 0
        xp_degisim = 0 
        
        if tip == "negatif":
            absorbe = (zeka / 350) 
            hasar = int(etki * (1 - absorbe))
            degisim = -hasar
            if secilen_kategori == "kritik": xp_degisim = -30
            else: xp_degisim = -random.randint(5, 10)
            icon = "🔻"
            renk_kodu = "red"
        else:
            degisim = etki
            if secilen_kategori == "kritik": xp_degisim = 50
            else: xp_degisim = random.randint(10, 20)
            icon = "💚"
            renk_kodu = "green"

        # Güncellemeler
        st.session_state.ruh_sagligi += degisim
        st.session_state.para += para_etkisi
        st.session_state.tecrube += xp_degisim
        st.session_state.gun_sayaci += 1
        
        if st.session_state.ruh_sagligi > 100: st.session_state.ruh_sagligi = 100
        st.session_state.gecmis_can.append(st.session_state.ruh_sagligi)

        p_txt = f" | {para_etkisi} TL" if para_etkisi != 0 else ""
        xp_txt = f" ({xp_degisim:+d} XP)"
        
        # Log Mesajı
        msg = f"**Gün {st.session_state.gun_sayaci-1}:** :{renk_kodu}[{olay_adi}] ({degisim} HP{p_txt}{xp_txt})"
        
        st.session_state.log.insert(0, msg)
        st.session_state.son_olay = f"{icon} {olay_adi} ({degisim} HP)"
        st.session_state.son_kategori = secilen_kategori

        if st.session_state.ruh_sagligi <= 0 or st.session_state.gun_sayaci > HEDEF_GUN:
            st.session_state.oyun_bitti = True
            st.session_state.kazandi = (st.session_state.ruh_sagligi > 0)
            st.rerun()

    if st.session_state.gun_sayaci > 1:
        if st.session_state.son_kategori == "kritik":
            st.error(f"🔥 KRİTİK GELİŞME: {st.session_state.son_olay}")
        elif st.session_state.son_kategori == "nadir":
            st.warning(f"📢 GELİŞME: {st.session_state.son_olay}")
        else:
            st.info(f"ℹ️ {st.session_state.son_olay}")

else:
    if not st.session_state.skor_kaydedildi:
        skor_kaydet(st.session_state.oyuncu_ismi, st.session_state.ruh_sagligi, st.session_state.tecrube)
        st.session_state.skor_kaydedildi = True 
        st.toast(f"Skor Tabloya İşlendi!")

    if st.session_state.kazandi:
        st.balloons()
        st.success(f"🎉 TEBRİKLER {st.session_state.oyuncu_ismi}!")
    else:
        st.error("💀 TÜKENDİN...")
    
    toplam_skor = st.session_state.ruh_sagligi + st.session_state.tecrube
    st.write(f"### 🏅 Toplam Skor: {toplam_skor}")
    
    st.write("### 📈 Ruh Sağlığı Grafiği")
    st.line_chart(st.session_state.gecmis_can)

    if st.button("🔄 Yeniden Başla"):
        st.session_state.ruh_sagligi = 100
        st.session_state.para = 1000
        st.session_state.gun_sayaci = 1
        st.session_state.tecrube = 0
        st.session_state.log = []
        st.session_state.gecmis_can = [100]
        st.session_state.oyun_bitti = False
        st.session_state.kazandi = False
        st.session_state.skor_kaydedildi = False 
        st.rerun()

if not st.session_state.oyun_bitti:
    st.write("### 📜 Olay Günlüğü")
    for satir in st.session_state.log[:5]:
        st.markdown(satir)