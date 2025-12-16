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
    else:
        st.sidebar.error("Paran Yok!")

if col_m2.button("🎧 Kulaklık (500)"):
    if st.session_state.para >= 500:
        st.session_state.para -= 500
        st.session_state.ruh_sagligi += 40
        if st.session_state.ruh_sagligi > 100: st.session_state.ruh_sagligi = 100
        st.sidebar.success("+40 Can")
        st.rerun()
    else:
        st.sidebar.error("Paran Yok!")

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
        
        # Grafik verisini kaydet
        st.session_state.gecmis_can.append(st.session_state.ruh_sagligi)

        # Log
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
    # --- OYUN SONU EKRANI (GRAFİK BURADA OLACAK) ---
    if st.session_state.kazandi:
        st.balloons()
        st.success(f"🎉 TEBRİKLER! {HEDEF_GUN} GÜN DAYANDIN!")
    else:
        st.error("💀 KAYBETTİN... Enerjin Tükendi.")
    
    # 1. GRAFİĞİ BURAYA KOYUYORUZ (Kesin Gözükecek)
    st.write("### 📈 Ruh Sağlığı Değişimi")
    chart_data = pd.DataFrame(st.session_state.gecmis_can, columns=["Ruh Sağlığı"])
    st.line_chart(chart_data)

    st.write(f"Toplam XP: {st.session_state.tecrube} | Kalan Para: {st.session_state.para} TL")

    # Yeniden Başlat
    if st.button("🔄 Yeniden Başla"):
        st.session_state.ruh_sagligi = 100
        st.session_state.para = 1000
        st.session_state.gun_sayaci = 1
        st.session_state.tecrube = 0
        st.session_state.log = []
        st.session_state.gecmis_can = [100]
        st.session_state.oyun_bitti = False
        st.session_state.kazandi = False
        st.rerun()

# --- GEÇMİŞ LOGLARI (SAYFA SONUNDA) ---
if not st.session_state.oyun_bitti:
    st.write("### 📜 Son Olaylar")
    for satir in st.session_state.log[:5]: # Sadece son 5 olayı göster ki sayfa uzamasın
        st.text(satir.replace("*", ""))