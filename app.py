import streamlit as st
import random
import pandas as pd # Grafikler için lazım

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Survivor: Niko's Economy", page_icon="🛡️", layout="centered")

# --- CSS (Makyaj) ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #FF512F 0%, #DD2476 100%);
        color: white !important;
        font-size: 20px;
        font-weight: bold;
        border-radius: 12px;
        border: none;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 6px 15px rgba(0,0,0,0.3);
    }
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 8px;
        border: 1px solid rgba(0, 0, 0, 0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- OYUN SABİTLERİ ---
HEDEF_GUN = 30 

# --- BAŞLIK ---
st.title(f"🛡️ Survivor: Ekonomi Modu")
st.markdown("**Görev:** 30 gün dayan. Paranla strateji yap, iflas etme, delirme.")

# --- SIDEBAR (KARAKTER & MARKET) ---
st.sidebar.header("👤 Profil")
isim = st.sidebar.text_input("İsim", "Niko")
zeka = st.sidebar.slider("Zeka (IQ)", 50, 160, 135)

# --- HAFIZA (SESSION STATE) ---
if 'ruh_sagligi' not in st.session_state: st.session_state.ruh_sagligi = 100
if 'para' not in st.session_state: st.session_state.para = 1000 # Başlangıç Parası
if 'gun_sayaci' not in st.session_state: st.session_state.gun_sayaci = 1
if 'tecrube' not in st.session_state: st.session_state.tecrube = 0
if 'log' not in st.session_state: st.session_state.log = []
if 'gecmis_can' not in st.session_state: st.session_state.gecmis_can = [100] # Grafik için
if 'oyun_bitti' not in st.session_state: st.session_state.oyun_bitti = False
if 'kazandi' not in st.session_state: st.session_state.kazandi = False

# --- MARKET SİSTEMİ (SIDEBAR) ---
st.sidebar.divider()
st.sidebar.header("🛒 Market")
st.sidebar.write(f"💰 Cüzdan: **{st.session_state.para} TL**")

col_market1, col_market2 = st.sidebar.columns(2)

if col_market1.button("☕ Kahve (200TL)"):
    if st.session_state.para >= 200:
        st.session_state.para -= 200
        st.session_state.ruh_sagligi += 15
        if st.session_state.ruh_sagligi > 100: st.session_state.ruh_sagligi = 100
        st.sidebar.success("Kahve içtin, ayıldın! (+15 HP)")
        st.rerun()
    else:
        st.sidebar.error("Paran yetersiz!")

if col_market2.button("🎧 Kulaklık (500TL)"):
    if st.session_state.para >= 500:
        st.session_state.para -= 500
        st.session_state.ruh_sagligi += 40
        if st.session_state.ruh_sagligi > 100: st.session_state.ruh_sagligi = 100
        st.sidebar.success("Dünyayı sessize aldın! (+40 HP)")
        st.rerun()
    else:
        st.sidebar.error("Paran yetersiz!")
        
st.sidebar.info("Marketten ürün alarak canını toparlayabilirsin.")


# --- DASHBOARD ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("❤️ Sağlık", f"{st.session_state.ruh_sagligi}")
c2.metric("💰 Bakiye", f"{st.session_state.para} TL")
c3.metric("📅 Gün", f"{st.session_state.gun_sayaci}/{HEDEF_GUN}")
c4.metric("✨ XP", st.session_state.tecrube)

st.progress(min(st.session_state.gun_sayaci / HEDEF_GUN, 1.0))

st.divider()

# --- OYUN AKIŞI ---

if not st.session_state.oyun_bitti:
    
    st.subheader(f"🌅 {st.session_state.gun_sayaci}. Gün")
    
    if st.button(f"Zarları At ve {st.session_state.gun_sayaci}. Günü Yaşa 🎲"):
        
        # Olay Havuzu: (Olay, Etki, Tip, Para Etkisi)
        # Para Etkisi: + para kazandırır, - para kaybettirir
        olaylar = [
            ("Maaş yattı!", 10, "pozitif", 5000),
            ("Yerde 100 TL buldun", 5, "pozitif", 100),
            ("Freelance işten ödeme geldi", 15, "pozitif", 2000),
            ("Markette her şeye zam gelmiş", 10, "negatif", -500),
            ("Kredi kartı borcu kesildi", 15, "negatif", -2000),
            ("Arkadaşın borcunu ödedi", 10, "pozitif", 500),
            ("Trafik cezası yedin", 20, "negatif", -1000),
            ("Bilgisayar bozuldu, tamir parası", 15, "negatif", -3000),
            
            # Parasız olaylar (Sadece psikolojik)
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
            renk = "red"
        else:
            degisim = etki
            icon = "💚"
            renk = "green"

        # Güncellemeler
        st.session_state.ruh_sagligi += degisim
        st.session_state.para += para_etkisi
        st.session_state.tecrube += 10
        st.session_state.gun_sayaci += 1
        
        # Sınır Kontrolleri
        if st.session_state.ruh_sagligi > 100: st.session_state.ruh_sagligi = 100
        
        # Grafik İçin Veri Kaydet
        st.session_state.gecmis_can.append(st.session_state.ruh_sagligi)

        # Log
        para_yazi = ""
        if para_etkisi != 0: para_yazi = f" | 💵 {para_etkisi} TL"
        
        log_mesaji = f"**Gün {st.session_state.gun_sayaci-1}:** :{renk}[{icon} {olay_adi}] ({degisim} HP{para_yazi})"
        st.session_state.log.insert(0, log_mesaji)

        # Bitiş Kontrolü
        if st.session_state.ruh_sagligi <= 0:
            st.session_state.ruh_sagligi = 0
            st.session_state.oyun_bitti = True
            st.session_state.kazandi = False
            st.rerun()
        elif st.session_state.gun_sayaci > HEDEF_GUN:
            st.session_state.oyun_bitti = True
            st.session_state.kazandi = True
            st.rerun()

else:
    if st.session_state.kazandi:
        st.balloons()
        st.success(f"🎉 TEBRİKLER! {HEDEF_GUN} GÜNÜ TAMAMLADIN!")
        st.write(f"Cüzdan: {st.session_state.para} TL | XP: {st.session_state.tecrube}")
    else:
        st.error("💀 OYUN BİTTİ... Enerjin tükendi.")
        
    if st.button("🔄 Yeniden Başla"):
        st.session_state.ruh_sagligi = 100
        st.session_state.para = 1000
        st.session_state.gun_sayaci = 1
        st.session_state.tecrube = 0
        st.session_state.log = []
        st.session_state.gecmis_can = [100]