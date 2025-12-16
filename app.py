import streamlit as st
import random
import pandas as pd
import os

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Survivor: Liderlik Tablosu", page_icon="🏆", layout="centered")

# --- CSS (GÖRÜNÜM) ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
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
</style>
""", unsafe_allow_html=True)

# --- SKOR KAYDETME FONKSİYONLARI ---
DOSYA_ADI = "skorlar.csv"

def skor_yukle():
    if not os.path.exists(DOSYA_ADI):
        return pd.DataFrame(columns=["İsim", "XP", "Gün"])
    return pd.read_csv(DOSYA_ADI)

def skor_kaydet(isim, xp, gun):
    df = skor_yukle()
    yeni_kayit = pd.DataFrame({"İsim": [isim], "XP": [xp], "Gün": [gun]})
    df = pd.concat([df, yeni_kayit], ignore_index=True)
    # XP'ye göre sırala (En yüksek en üstte)
    df = df.sort_values(by="XP", ascending=False)
    # Sadece ilk 10'u sakla
    df = df.head(10)
    df.to_csv(DOSYA_ADI, index=False)

# --- OYUN SABİTLERİ ---
HEDEF_GUN = 30 

# --- BAŞLIK ---
st.title(f"🛡️ Survivor: Liderlik Savaşı")

# --- SIDEBAR (PROFİL & SKORBORD) ---
st.sidebar.header("👤 Oyuncu")
# Session state kullanarak ismin değişmemesini sağlıyoruz
if 'oyuncu_ismi' not in st.session_state:
    st.session_state.oyuncu_ismi = "Niko"

isim_input = st.sidebar.text_input("İsminiz:", st.session_state.oyuncu_ismi)
st.session_state.oyuncu_ismi = isim_input

zeka = st.sidebar.slider("Zeka (IQ)", 50, 160, 135)

# --- LİDERLİK TABLOSU GÖSTERİMİ ---
st.sidebar.divider()
st.sidebar.header("🏆 Top 10 Liderler")
df_skor = skor_yukle()
if not df_skor.empty:
    st.sidebar.dataframe(df_skor, hide_index=True)
else:
    st.sidebar.info("Henüz kimse listeye girmedi. İlk sen ol!")

# --- OYUN DEĞİŞKENLERİ ---
if 'ruh_sagligi' not in st.session_state: st.session_state.ruh_sagligi = 100
if 'para' not in st.session_state: st.session_state.para = 1000 
if 'gun_sayaci' not in st.session_state: st.session_state.gun_sayaci = 1
if 'tecrube' not in st.session_state: st.session_state.tecrube = 0
if 'log' not in st.session_state: st.session_state.log = []
if 'gecmis_can' not in st.session_state: st.session_state.gecmis_can = [100] 
if 'oyun_bitti' not in st.session_state: st.session_state.oyun_bitti = False
if 'kazandi' not in st.session_state: st.session_state.kazandi = False
if 'son_olay' not in st.session_state: st.session_state.son_olay = "Başlangıç..."
if 'skor_kaydedildi' not in st.session_state: st.session_state.skor_kaydedildi = False

# --- MARKET ---
st.sidebar.divider()
st.sidebar.header("🛒 Market")
st.sidebar.write(f"💰 Cüzdan: **{st.session_state.para} TL**")

col_m1, col_m2 = st.sidebar.columns(2)
if col_m1.button("☕ Kahve (200)"):
    if st.session_state.para >= 200:
        st.session_state.para -= 200
        st.session_state.ruh_sagligi += 15
        if st.session_state.ruh_sagligi > 100: st.session_state.ruh_sagligi = 100
        st.sidebar.success("Can Yenilendi!")
        st.rerun()
if col_m2.button("🎧 Kulaklık (500)"):
    if st.session_state.para >= 500:
        st.session_state.para -= 500
        st.session_state.ruh_sagligi += 40
        if st.session_state.ruh_sagligi > 100: st.session_state.ruh_sagligi = 100
        st.sidebar.success("Can Yenilendi!")
        st.rerun()

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
    
    # BUTON
    if st.button(f"🎲 Zarları At ve Günü Yaşa"):
        olaylar = [
            ("Maaş yattı!", 10, "pozitif", 5000),
            ("Yerde 100 TL buldun", 5, "pozitif", 100),
            ("Freelance işten ödeme geldi", 15, "pozitif", 2000),
            ("Markette her şeye zam gelmiş", 10, "negatif", -500),
            ("Kredi kartı borcu kesildi", 15, "negatif", -2000),
            ("Trafik cezası yedin", 20, "negatif", -1000),
            ("Bilgisayar bozuldu", 15, "negatif", -3000),
            ("Patron boş konuştu", 20, "negatif", 0),
            ("Kod tek seferde çalıştı", 20, "pozitif", 0),
            ("Kedi sevdin", 15, "pozitif", 0),
            ("Uykusuz kaldın", 25, "negatif", 0),
            ("Güzel bir duş aldın", 15, "pozitif", 0),
            ("İftira atıldı", 40, "negatif", 0),
            ("Eski dost aradı", 20, "pozitif", 0)
        ]
        
        olay_adi, etki, tip, para_etkisi = random.choice(olaylar)
        
        degisim = 0
        if tip == "negatif":
            absorbe = (zeka / 350) 
            hasar = int(etki * (1 - absorbe))
            degisim = -hasar
            icon = "🔻"
        else:
            degisim = etki
            icon = "💚"

        # Güncellemeler
        st.session_state.ruh_sagligi += degisim
        st.session_state.para += para_etkisi
        st.session_state.tecrube += 10
        st.session_state.gun_sayaci += 1
        
        if st.session_state.ruh_sagligi > 100: st.session_state.ruh_sagligi = 100
        
        st.session_state.gecmis_can.append(st.session_state.ruh_sagligi)

        p_txt = f" | {para_etkisi} TL" if para_etkisi != 0 else ""
        msg = f"**Gün {st.session_state.gun_sayaci-1}:** {icon} {olay_adi} ({degisim} HP{p_txt})"
        st.session_state.log.insert(0, msg)
        st.session_state.son_olay = msg

        # Oyun Bitti mi?
        if st.session_state.ruh_sagligi <= 0 or st.session_state.gun_sayaci > HEDEF_GUN:
            st.session_state.oyun_bitti = True
            st.session_state.kazandi = (st.session_state.ruh_sagligi > 0)
            st.rerun()

    if st.session_state.gun_sayaci > 1:
        st.info(f"📢 {st.session_state.son_olay}")

else:
    # --- OYUN SONU (SKOR KAYDETME YERİ) ---
    
    # Skoru daha önce kaydetmediysek şimdi kaydet
    if not st.session_state.skor_kaydedildi:
        skor_kaydet(st.session_state.oyuncu_ismi, st.session_state.tecrube, st.session_state.gun_sayaci-1)
        st.session_state.skor_kaydedildi = True # Tekrar kaydetmeyi engelle
        st.toast(f"Skor Kaydedildi: {st.session_state.oyuncu_ismi} - {st.session_state.tecrube} XP")

    if st.session_state.kazandi:
        st.balloons()
        st.success(f"🎉 TEBRİKLER {st.session_state.oyuncu_ismi}! Liderlik Tablosuna Girdin!")
    else:
        st.error("💀 KAYBETTİN... Ama skorun tabloya işlendi.")
    
    st.write("### 📈 Ruh Sağlığı Değişimi")
    st.line_chart(st.session_state.gecmis_can)
    st.write(f"Toplam XP: **{st.session_state.tecrube}**")

    # Yeniden Başlat
    if st.button("🔄 Yeniden Başla"):
        # Her şeyi sıfırla
        st.session_state.ruh_sagligi = 100
        st.session_state.para = 1000
        st.session_state.gun_sayaci = 1
        st.session_state.tecrube = 0
        st.session_state.log = []
        st.session_state.gecmis_can = [100]
        st.session_state.oyun_bitti = False
        st.session_state.kazandi = False
        st.session_state.skor_kaydedildi = False # Yeni oyun için kilidi aç
        st.rerun()

if not st.session_state.oyun_bitti:
    st.write("### 📜 Son Olaylar")
    for satir in st.session_state.log[:5]:
        st.text(satir.replace("*", ""))