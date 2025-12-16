import streamlit as st
import random
import time

# Sayfa Ayarları
st.set_page_config(page_title="Survivor: Niko's Edition", page_icon="🛡️")

# Başlık ve Giriş
st.title("🛡️ Survivor Simülasyonu")
st.write("Hayat zor, ama algoritma daha zor. Bakalım karakterin ne kadar dayanacak?")

# Sidebar (Sol Menü) - Karakter Oluşturma
st.sidebar.header("Karakterini Yarat")
isim = st.sidebar.text_input("Karakter Adı", "Niko")
zeka = st.sidebar.slider("Zeka Seviyesi (IQ)", 50, 150, 120)
dayaniklilik = st.sidebar.slider("Ruhsal Dayanıklılık", 0, 100, 80)

# Session State (Verileri hafızada tutmak için)
if 'ruh_sagligi' not in st.session_state:
    st.session_state.ruh_sagligi = 100
if 'tecrube' not in st.session_state:
    st.session_state.tecrube = 0
if 'log' not in st.session_state:
    st.session_state.log = []

# Ana Ekran Göstergeleri
col1, col2, col3 = st.columns(3)
col1.metric("Ruh Sağlığı", f"{st.session_state.ruh_sagligi}%")
col2.metric("Tecrübe Puanı (XP)", st.session_state.tecrube)
col3.metric("Durum", "Savaşçı" if st.session_state.ruh_sagligi > 20 else "KRİTİK! 🚨")

# Aksiyon Butonu
st.divider()
st.subheader("🔥 Hayatla Yüzleş")

if st.button("Rastgele Bir Sorunla Karşılaş"):
    # Sorun Havuzu
    sorunlar = [
        ("Mobbing Yedin", 80),
        ("Yanlışlıkla Production DB'yi sildin", 90),
        ("Maaş geç yattı", 40),
        ("Trafikte kaldın", 20),
        ("İftira atıldı", 100)
    ]
    
    olay, zorluk = random.choice(sorunlar)
    
    # SENİN FORMÜLÜN BURADA DEVREYE GİRİYOR
    # Zeka ne kadar yüksekse, hasarı o kadar absorbe eder (Basit bir mantık)
    # Zeka 100 ise hasarı %50 azaltır, Zeka 150 ise %75 azaltır gibi.
    absorbe_orani = (zeka / 200) 
    alinan_hasar = int(zorluk * (1 - absorbe_orani))
    
    # Dayanıklılık bonusu: Eğer dayanıklılık yüksekse kritik hasar almaz
    if dayaniklilik > 80:
        alinan_hasar -= 5
    
    if alinan_hasar < 0: alinan_hasar = 0

    # Güncelleme
    st.session_state.ruh_sagligi -= alinan_hasar
    st.session_state.tecrube += int(zorluk / 2)
    
    # Loglama
    yeni_log = f"🛑 **OLAY:** {olay} (Zorluk: {zorluk}) -> **Hasar:** -{alinan_hasar} HP | **Kazanılan XP:** +{int(zorluk/2)}"
    st.session_state.log.insert(0, yeni_log) # En yeniyi başa ekle

    if st.session_state.ruh_sagligi <= 0:
        st.error("💀 OYUN BİTTİ! Karakter tükendi.")
        st.session_state.ruh_sagligi = 0
    else:
        st.success("Hala ayaktasın! Direnmeye devam.")

# Geçmiş Logları Yazdır
st.divider()
st.write("### 📜 Savaş Günlüğü")
for log in st.session_state.log:
    st.markdown(log)

# Sıfırlama Butonu
if st.button("Simülasyonu Sıfırla"):
    st.session_state.ruh_sagligi = 100
    st.session_state.tecrube = 0
    st.session_state.log = []
    st.rerun()