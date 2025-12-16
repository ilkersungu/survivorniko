import streamlit as st
import random
import pandas as pd # Grafiği garantiye almak için geri çağırdık

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Survivor: Niko's Destiny", page_icon="🛡️", layout="centered")

# --- CSS (GÖRÜNÜM) ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%); /* Mavi Tonları */
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

# --- OYUN SABİTLERİ ---
HEDEF_GUN = 30 

# --- BAŞLIK ---
st.title(f"🛡️ Survivor: 30 Gün Mücadelesi")
st.markdown("**Görev:** 30 gün dayan. Grafiğini yukarıda tut!")

# --- SIDEBAR ---
st.sidebar.header("👤 Profil")
isim = st.sidebar.text_input("İsim", "Niko")
zeka = st.sidebar.slider("Zeka (IQ)", 50, 160, 135)

# --- HAFIZA (SESSION STATE) ---
if 'ruh_sagligi' not in st.session_state: st.session_state.ruh_sagligi = 100
if 'para' not in st.session_state: st.session_state.para = 1000 
if 'gun_sayaci' not in st.session_state: st.session_state.gun_sayaci = 1
if 'tecrube' not in st.session_state: st.session_state.tecrube = 0
if 'log' not in st.session_state: st.session_state.log = []
# Grafiği çizmek için veriyi burada tutuyoruz:
if 'gecmis_can' not in st.session_state: st.session_state.gecmis_can = [100] 
if 'oyun_bitti' not in st.session_state: st.session_state.oyun_bitti = False
if 'kazandi' not in st.session_state: st.session_state.kazandi = False
if 'son_olay' not in st.session_state: st.session_state.son_olay = "Başlangıç..."

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
        st.sidebar.success("+15 Can")
        st.rerun()
if col_m2.button("🎧