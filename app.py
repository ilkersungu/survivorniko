import streamlit as st
import random
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Survivor: Niko's Challenge", page_icon="🛡️", layout="centered")

# --- CSS İLE MAKYAJ (DÜZELTİLDİ) ---
st.markdown("""
<style>
    /* Arka plan rengini sildik, senin teman neyse o kalsın */
    
    /* O Büyük Butonu Tasarlayalım */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #FF512F 0%, #DD2476 100%); /* Turuncu-Pembe Geçiş */
        color: white !important; /* Yazı rengini beyaza zorla */
        font-size: 24px;
        font-weight: bold;
        padding: 15px 30px;
        border-radius: 15px;
        border: none;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    /* Üzerine gelince ne olsun? */
    .stButton>button:hover {
        transform: translateY(-2px); /* Hafif yukarı zıplasın */
        box-shadow: 0px 6px 20px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #DD2476 0%, #FF512F 100%); 
        color: white !important;
    }

    /* İstatistik Kutuları */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.1); /* Hafif şeffaf beyaz */
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- OYUN SABİTLERİ ---
HEDEF_GUN = 30 

# --- BAŞLIK ---
st.title(f"🛡️ Survivor: {HEDEF_GUN} Gün Challenge")
st.markdown("**Görev:** 30 gün boyunca kaosun içinde hayatta kal. Enerjin biterse, oyun biter.")

# --- KENAR ÇUBUĞU ---
st.sidebar.header("👤 Karakter Ayarları")
isim = st.sidebar.text_input("İsim", "Niko")
zeka = st.sidebar.slider("Zeka (IQ)", 50, 160, 135)
st.sidebar.info("Not: Yüksek Zeka, negatif olaylardan aldığın hasarı azaltır.")

# --- HAFIZA (SESSION STATE) ---
if 'ruh_sagligi' not in st.session_state: st.session_state.ruh_sagligi = 100
if 'gun_sayaci' not in st.session_state: st.session_state.gun_sayaci = 1
if 'tecrube' not in st.session_state: st.session_state.tecrube = 0
if 'log' not in st.session_state: st.session_state.log = []
if 'oyun_bitti' not in st.session_state: st.session_state.oyun_bitti = False
if 'kazandi' not in st.session_state: st.session_state.kazandi = False

# --- GÖSTERGE PANELİ (DASHBOARD) ---
col1, col2, col3 = st.columns(3)
col1.metric("❤️ Ruh Sağlığı", f"{st.session_state.ruh_sagligi}")
col2.metric("📅 Gün", f"{st.session_state.gun_sayaci} / {HEDEF_GUN}")
col3.metric("✨ XP Puanı", st.session_state.tecrube)

# İlerleme Çubuğu
ilerleme = min(st.session_state.gun_sayaci / HEDEF_GUN, 1.0)
st.progress(ilerleme)

st.divider()

# --- OYUN MANTIĞI ---

if not st.session_state.oyun_bitti:
    
    st.subheader(f"🌅 {st.session_state.gun_sayaci}. Günün Sabahı")
    
    # BUTON
    if st.button(f"Zarları At ve {st.session_state.gun_sayaci}. Günü Yaşa 🎲"):
        
        # OLAY HAVUZU
        olaylar = [
            ("Patron 'Acil toplantı' dedi, 2 saat boş konuştu", 20, "negatif"),
            ("Production veritabanını yanlışlıkla sildin", 50, "negatif"),
            ("Maaş gününde ödeme yapılmadı", 25, "negatif"),
            ("Sabah trafiğinde 2 saat kilitli kaldın", 15, "negatif"),
            ("Gece eski travmalar uykunu böldü", 30, "negatif"),
            ("Ofiste üzerine kahve döküldü", 10, "negatif"),
            ("Kodun çalışmıyor ve nedenini bulamıyorsun", 15, "negatif"),
            ("En güvendiğin arkadaşın seni sattı", 40, "negatif"),
            ("Bilgisayarın mavi ekran verdi", 25, "negatif"),
            ("Markete gittin, her şeye zam gelmiş", 10, "negatif"),
            ("Anlamsız bir mide bulantısı başladı", 20, "negatif"),
            ("Birisi arkandan dedikodu yapmış", 30, "negatif"),
            ("Hafta sonu zorunlu mesai çıktı", 35, "negatif"),
            ("İnternet kesildi, işler yetişmiyor", 15, "negatif"),
            ("Yanlışlıkla tüm şirkete 'Reply All' yaptın", 45, "negatif"),
            ("Sokakta bir kedi bacağına sürtündü", 15, "pozitif"),
            ("Kodun 'Bug'sız tek seferde çalıştı!", 30, "pozitif"),
            ("Hesabına beklenmedik bir para yattı", 35, "pozitif"),
            ("Patron bugün işe gelmedi, ofis rahat", 20, "pozitif"),
            ("Çok güzel bir gün batımı izledin", 10, "pozitif"),
            ("Eski bir dost arayıp halini sordu", 20, "pozitif"),
            ("Bu gece deliksiz ve rüyasız uyudun", 40, "pozitif"),
            ("Yolda yürürken kaldırımda açan inatçı bir çiçek gördün", 15, "pozitif"),
            ("Zor bir problemi zekanca çözdün", 25, "pozitif"),
            ("Radyoda en sevdiğin şarkı çaldı", 10, "pozitif"),
            ("Sıcak, harika bir duş aldın", 15, "pozitif"),
            ("Birisi sana 'İyi ki varsın' dedi", 35, "pozitif"),
            ("Trafik şaşırtıcı derecede açık", 10, "pozitif"),
            ("Hafta sonu tatili başladı!", 25, "pozitif"),
            ("Maaşına sürpriz zam yapıldı", 50, "pozitif")
        ]
        
        olay_adi, etki_puani, olay_tipi = random.choice(olaylar)
        degisim = 0
        
        if olay_tipi == "negatif":
            absorbe = (zeka / 350) 
            hasar = int(etki_puani * (1 - absorbe))
            degisim = -hasar
            icon = "🔻"
            renk = "red"
        else:
            degisim = etki_puani
            icon = "💚"
            renk = "green"

        st.session_state.ruh_sagligi += degisim
        st.session_state.tecrube += 10
        st.session_state.gun_sayaci += 1
        
        if st.session_state.ruh_sagligi > 100: st.session_state.ruh_sagligi = 100

        log_mesaji = f"**Gün {st.session_state.gun_sayaci-1}:** :{renk}[{icon} {olay_adi}] ({degisim} HP)"
        st.session_state.log.insert(0, log_mesaji)

        # KONTROLLER
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
    # OYUN BİTTİ EKRANI
    if st.session_state.kazandi:
        st.balloons()
        st.success(f"🎉 TEBRİKLER! {HEDEF_GUN} GÜNÜ TAMAMLADIN!")
        st.write(f"Toplam XP: {st.session_state.tecrube}")
    else:
        st.error("💀 OYUN BİTTİ... Enerjin tükendi.")
        st.write(f"{st.session_state.gun_sayaci}. Güne kadar gelebildin.")

    # Yeniden Başlat Butonu
    if st.button("🔄 Yeniden Başla"):
        st.session_state.ruh_sagligi = 100
        st.session_state.gun_sayaci = 1
        st.session_state.tecrube = 0
        st.session_state.log = []
        st.session_state.oyun_bitti = False
        st.session_state.kazandi = False
        st.rerun()

# --- LOGLAR ---
st.write("### 📜 Olay Günlüğü")
for satir in st.session_state.log:
    st.markdown(satir)