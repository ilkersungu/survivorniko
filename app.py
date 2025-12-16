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
DOSYA_ADI = "skorlar_v3_nikonun30gunu.csv" 

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
    df = df.head(10)
    df.to_csv(DOSYA_ADI, index=False)

# --- OYUN SABİTLERİ ---
HEDEF_GUN = 30 

# --- BAŞLIK ---
st.title(f"🛡️ Survivor: Niko'nun 30 Günü")
st.markdown("**Hedef:** 30 gün boyunca hayatta kal. Şansını değil, sabrını test et.")

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
    st.sidebar.info("Tablo boş.")

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
if 'skor_kaydedildi' not in st.session_state: st.session_state.skor_kaydedildi = False

# --- MARKET ---
st.sidebar.divider()
st.sidebar.header("🛒 Market")
st.sidebar.write(f"💰 Bakiye: **{st.session_state.para} TL**")
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
c1.metric("❤️