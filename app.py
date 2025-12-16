import streamlit as st
import random

# Sayfa Ayarları
st.set_page_config(page_title="Survivor: Niko's Edition", page_icon="🛡️")

# Başlık
st.title("🛡️ Survivor Simülasyonu v3.0 (Extended)")
st.write("Hayat bir kaos teorisidir. Bakalım rastgelelik seni nereye götürecek?")

# --- KENAR ÇUBUĞU (AYARLAR) ---
st.sidebar.header("Karakterini Yarat")
isim = st.sidebar.text_input("Karakter Adı", "Niko")
zeka = st.sidebar.slider("Zeka Seviyesi (IQ)", 50, 160, 135)

# --- HAFIZA (SESSION STATE) ---
if 'ruh_sagligi' not in st.session_state:
    st.session_state.ruh_sagligi = 100
if 'tecrube' not in st.session_state:
    st.session_state.tecrube = 0
if 'log' not in st.session_state:
    st.session_state.log = []
if 'oyun_bitti' not in st.session_state:
    st.session_state.oyun_bitti = False

# --- ANA GÖSTERGELER ---
col1, col2, col3 = st.columns(3)
col1.metric("❤️ Ruh Sağlığı", f"{st.session_state.ruh_sagligi}")
col2.metric("✨ Tecrübe (XP)", st.session_state.tecrube)

durum_yazisi = "Savaşçı"
if st.session_state.ruh_sagligi <= 30: durum_yazisi = "Yorgun..."
if st.session_state.ruh_sagligi <= 10: durum_yazisi = "SON DEMLER!"
if st.session_state.ruh_sagligi <= 0: durum_yazisi = "MEFTA"

col3.metric("Durum", durum_yazisi)

st.divider()

# --- OYUN MANTIĞI ---

if st.session_state.ruh_sagligi > 0:
    st.subheader("🎲 Kader Çarkını Çevir")
    
    if st.button("Günü Yaşa"):
        # GENİŞLETİLMİŞ OLAY HAVUZU (40 ADET)
        # Format: ("Olay Adı", Etki Puanı, "Tip")
        olaylar = [
            # --- NEGATİF OLAYLAR (HAYATIN SİLLELERİ) ---
            ("Patron sebepsiz yere bağırdı", 25, "negatif"),
            ("Yanlışlıkla Production DB'yi uçurdun", 40, "negatif"),
            ("Maaş yine geç yattı", 20, "negatif"),
            ("Trafikte 2 saat adım atılmadı", 15, "negatif"),
            ("Eski travmalar gece uykunu kaçırdı", 30, "negatif"),
            ("İş yerinde dedikodu yapıldı, ihale sana kaldı", 35, "negatif"),
            ("Markete gittin, her şeye %50 zam gelmiş", 15, "negatif"),
            ("Yazdığın kod çalışmadı, hatayı bulamıyorsun", 10, "negatif"),
            ("Annenle telefonda gergin bir konuşma geçti", 25, "negatif"),
            ("Mide bulantısı ve anksiyete atağı", 20, "negatif"),
            ("Bilgisayar tam sunum yaparken mavi ekran verdi", 20, "negatif"),
            ("En sevdiğin gömleğe kahve döküldü", 5, "negatif"),
            ("Yağmura yakalandın, şemsiye yok", 10, "negatif"),
            ("Kredi kartı ekstresi beklediğinden yüksek geldi", 25, "negatif"),
            ("Birisi zekanı küçümseyen bir laf etti", 30, "negatif"),
            ("İnternet kesildi, işler yetişmiyor", 15, "negatif"),
            ("Hafta sonu mesaiye çağrıldın", 35, "negatif"),
            ("Yanlış kişiye güvendin", 40, "negatif"),
            ("Klimadan boynun tutuldu", 10, "negatif"),
            
            # --- POZİTİF OLAYLAR (NEFES ALDIRANLAR) ---
            ("Sokakta bir kedi yanına gelip kendini sevdirdi", 15, "pozitif"),
            ("Kodun 'Warning' bile vermeden tek seferde çalıştı", 25, "pozitif"),
            ("Hesapta olmayan bir para geldi", 30, "pozitif"),
            ("Patron bugün ofise gelmedi!", 20, "pozitif"),
            ("Çok güzel bir gün batımı yakaladın", 10, "pozitif"),
            ("Eski bir dost arayıp halini hatrını sordu", 20, "pozitif"),
            ("Gece deliksiz ve rüyasız uyudun", 35, "pozitif"),
            ("Yolda yürürken kaldırımda açan bir çiçek gördün", 15, "pozitif"),
            ("Zor bir problemi zekanca çözdün, herkes şaşırdı", 25, "pozitif"),
            ("Radyoda en sevdiğin şarkı çaldı", 10, "pozitif"),
            ("Sıcak, güzel bir duş aldın", 15, "pozitif"),
            ("Birisi sana 'İyi ki varsın' dedi", 30, "pozitif"),
            ("Trafik şaşırtıcı derecede açık", 10, "pozitif"),
            ("Hafta sonu tatili başladı", 20, "pozitif"),
            ("En sevdiğin tatlıyı yedin", 10, "pozitif"),
            ("Dışarıda mis gibi yağmur sonrası toprak kokusu var", 15, "pozitif"),
            ("Maaşına beklenmedik bir zam yapıldı", 40, "pozitif"),
            ("Bugün kimse seni darlamadı, sakin bir gün", 20, "pozitif")
        ]
        
        olay_adi, etki_puani, olay_tipi = random.choice(olaylar)
        
        degisim = 0
        
        if olay_tipi == "negatif":
            # Zeka faktörü: Yüksek zeka hasarı yumuşatır
            absorbe = (zeka / 350) 
            hasar = int(etki_puani * (1 - absorbe))
            degisim = -hasar
            icon = "🔻"
            renk = "red"
        else:
            degisim = etki_puani
            icon = "💚"
            renk = "green"

        # Güncelleme
        st.session_state.ruh_sagligi += degisim
        st.session_state.tecrube += 10
        
        # Sınır Kontrolü
        if st.session_state.ruh_sagligi > 100: st.session_state.ruh_sagligi = 100

        # Loglama (Renkli ve İkonlu)
        log_mesaji = f":{renk}[{icon} **{olay_adi}**] ({degisim} HP)"
        st.session_state.log.insert(0, log_mesaji)

        # Game Over
        if st.session_state.ruh_sagligi <= 0:
            st.session_state.ruh_sagligi = 0
            st.session_state.oyun_bitti = True
            st.rerun()

else:
    st.error("💀 OYUN BİTTİ! Ruhsal sermaye tükendi.")
    st.info(f"🏆 Toplam Kazanılan Tecrübe: **{st.session_state.tecrube} XP**")
    
    if st.button("🔄 Yeniden Doğ (Reborn)"):
        st.session_state.ruh_sagligi = 100
        st.session_state.tecrube = 0
        st.session_state.log = []
        st.session_state.oyun_bitti = False
        st.rerun()

# --- GEÇMİŞ ---
st.write("### 📜 Savaş Günlüğü")
for satir in st.session_state.log:
    st.markdown(satir)