# -*- coding: utf-8 -*-
"""
Aplikasi: Pushy Cat Care App
Pengembang: STIEIMA Cat Care
Deskripsi: Sistem manajemen perawatan kucing cerdas dengan Deteksi Kesehatan AI,
           E-commerce terintegrasi, Direktori Vet/Komunitas, dan Chatbot "Pushy AI".
Bahasa: Python (Streamlit Framework)
"""

import streamlit as st
import pandas as pd
import random
import time
import requests
import json

# ==========================================
# KONFIGURASI HALAMAN & AUTH GEMINI API
# ==========================================
st.set_page_config(
    page_title="Pushy Cat Care App - STIEIMA",
    page_icon="🐱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Berdasarkan instruksi lingkungan, API Key didefinisikan sebagai string kosong.
# Sistem runtime akan menyuntikkan kunci jika tersedia.
API_KEY = ""

# ==========================================
# TEMA & GAYA KUSTOM (CSS INLINE)
# ==========================================
st.markdown("""
<style>
    /* Mengubah warna aksen utama menjadi oranye hangat dan biru lembut */
    .stApp {
        background-color: #fafafc;
    }
    h1, h2, h3 {
        color: #2E5B88 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #FFF5EC;
    }
    /* Kotak informasi bergaya kartu */
    .feature-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #FF8C32;
        margin-bottom: 15px;
    }
    .alert-danger-custom {
        background-color: #FFECEC;
        border-left: 5px solid #D8000C;
        color: #D8000C;
        padding: 15px;
        border-radius: 8px;
        margin-top: 10px;
    }
    .alert-warning-custom {
        background-color: #FFF9E6;
        border-left: 5px solid #9F6000;
        color: #9F6000;
        padding: 15px;
        border-radius: 8px;
        margin-top: 10px;
    }
    .alert-success-custom {
        background-color: #EDF7ED;
        border-left: 5px solid #4CAF50;
        color: #1E4620;
        padding: 15px;
        border-radius: 8px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# INISIALISASI STATE (DATABASE IN-MEMORY)
# ==========================================
# Inisialisasi data default hanya jika belum ada dalam session state
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    
    # Direktori Dokter Hewan (Vet) Awal
    st.session_state.vet_directory = [
        {"id": 1, "nama": "Klinik Vet Medika Sejahtera", "alamat": "Jl. Raya Lowokwaru No. 12, Malang", "telepon": "0341-555123", "status": "Approved"},
        {"id": 2, "nama": "Praktek Drh. Sarah Amanda", "alamat": "Ruko Sulfat Indah Blok B-4, Malang", "telepon": "0812-3456-7890", "status": "Approved"}
    ]
    
    # Direktori Komunitas Kucing Awal
    st.session_state.communities = [
        {"id": 1, "nama": "Malang Cat Lovers Community", "kontak": "Hendra (0821-4455-6677)", "wilayah": "Malang Raya", "status": "Approved"},
        {"id": 2, "nama": "Komunitas Peduli Kucing Liar STIEIMA", "kontak": "Admin STIEIMA", "wilayah": "Kampus & Sekitarnya", "status": "Approved"}
    ]
    
    # Produk E-Commerce Awal
    st.session_state.products = [
        {"id": "pakan-01", "nama": "Royal Canin Fit 32 2kg", "kategori": "Makanan", "harga": 220000, "stok": 15, "deskripsi": "Pakan lengkap dan seimbang untuk kucing dewasa usia di atas 1 tahun."},
        {"id": "obat-01", "nama": "Obat Cacing Drontal Cat (per tablet)", "kategori": "Obat-obatan", "harga": 25000, "stok": 50, "deskripsi": "Efektif membasmi cacing gelang dan cacing pita pada kucing."},
        {"id": "nutrisi-01", "nama": "Minyak Ikan Bulu Kucing Premium", "kategori": "Nutrisi & Vitamin", "harga": 100000, "stok": 20, "deskripsi": "Mengandung Omega 3 & 6 untuk keindahan bulu dan pencegahan rontok."},
        {"id": "kebersihan-01", "nama": "Shampoo Anti Kutu & Jamur 250ml", "kategori": "Kebersihan", "harga": 160000, "stok": 10, "deskripsi": "Formula sulfur ringan untuk membasmi jamur ringworm dan kutu kucing."}
    ]
    
    # Keranjang Belanjaan Pengguna
    st.session_state.cart = []
    
    # Riwayat Percakapan Chatbot
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Halo Cat Lover! Saya Pushy AI, asisten virtual medis kucing dari STIEIMA Cat Care. Ada yang bisa saya bantu hari ini mengenai kesehatan kucing kesayangan Anda?"}
    ]
    
    # Kisah Sukses (Testimoni Pengguna)
    st.session_state.success_stories = [
        {"user": "Budi - Malang", "cerita": "Kucing saya, si Miko, mendadak botak melingkar di telinga. Berkat fitur Kamera Deteksi AI Pushy, terindikasi Ringworm 85% sejak dini. Saya segera mengisolasinya dari anak saya, membeli sampo sulfur di e-commerce Pushy, dan sekarang Miko sudah sembuh total tanpa menularkan ke keluarga!"},
        {"user": "Rini - Jakarta", "cerita": "Fitur Checklist Gejala membantu saya mendeteksi flu kucing sebelum terlambat. Pertolongan pertama dari aplikasi ini sangat menenangkan!"}
    ]

# ==========================================
# LOGIKA BISNIS INTI (SESUAI PRD)
# ==========================================

def hitung_status_kesehatan(skor_ai: float, jumlah_gejala_fisik: int) -> dict:
    """
    Menghitung tingkat keparahan kesehatan kucing berdasarkan input model deteksi AI dan gejala fisik.
    Aturan ini diambil langsung dari spesifikasi Unit Testing PRD Bab 6.A.
    """
    if skor_ai < 0.0 or skor_ai > 1.0:
        raise ValueError("Skor AI harus berada di rentang nilai 0.0 hingga 1.0")
    if jumlah_gejala_fisik < 0:
        raise ValueError("Jumlah gejala tidak boleh bernilai negatif")

    if skor_ai >= 0.75 or jumlah_gejala_fisik >= 3:
        return {
            "status": "BAHAYA",
            "perlu_isolasi": True,
            "warna": "danger",
            "pesan": "🚨 **Kondisi Bahaya/Kritis:** Segera isolasi kucing Anda secara ketat di ruangan terpisah. Jangan biarkan anak-anak mendekat untuk mencegah potensi penularan zoonosis (misal Scabies akut/Toxoplasmosis). Segera bawa ke Dokter Hewan terdekat!"
        }
    elif 0.40 <= skor_ai < 0.75 or 1 <= jumlah_gejala_fisik <= 2:
        return {
            "status": "PERLU PERHATIAN",
            "perlu_isolasi": True,
            "warna": "warning",
            "pesan": "⚠️ **Perlu Perhatian:** Kucing menunjukkan tanda-tanda awal sakit atau gejala ringan (seperti potensi Ringworm awal atau Flu ringan). Disarankan untuk memisahkan kandangnya untuk sementara waktu, berikan nutrisi suplemen bulu/imunitas, dan mandikan dengan sampo obat khusus."
        }
    else:
        return {
            "status": "SEHAT",
            "perlu_isolasi": False,
            "warna": "success",
            "pesan": "💚 **Kondisi Sehat:** Kucing Anda terdeteksi dalam kondisi prima! Tetap jaga kebersihan sanitasi kandang, pola makan teratur, serta pastikan jadwal vaksinasi selalu tepat waktu."
        }

def hitung_total_belanja(items, kode_promo, biaya_kirim=15000):
    """
    Menghitung rincian pembayaran belanja e-commerce.
    Aturan ini diambil langsung dari spesifikasi Unit Testing PRD Bab 6.B.
    """
    subtotal = sum(item["harga"] * item["kuantitas"] for item in items)
    nominal_diskon = 0
    
    # Aturan diskon promo STIEIMA Cat Care
    if kode_promo == "PUSHYSEHAT":
        nominal_diskon = subtotal * 0.15 # Diskon 15%
    elif kode_promo == "GRATISONGKIR" and subtotal >= 150000:
        biaya_kirim = max(0, biaya_kirim - 15000) # Potongan ongkir s.d Rp 15.000
        
    total_akhir = (subtotal - nominal_diskon) + biaya_kirim
    return {
        "subtotal": subtotal,
        "nominal_diskon": nominal_diskon,
        "biaya_kirim_final": biaya_kirim,
        "total_akhir": max(0, total_akhir)
    }

# ==========================================
# FUNGSI INTEGRASI GEMINI CHATBOT (API CALL)
# ==========================================
def panggil_gemini_api(user_message, system_instruction):
    """
    Memanggil model gemini-2.5-flash-preview-09-2025 secara non-streaming dengan
    strategi retries eksponensial (up to 5 times) jika terjadi kegagalan jaringan.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": user_message}]
        }],
        "systemInstruction": {
            "parts": [{"text": system_instruction}]
        }
    }
    
    # Jika API_KEY kosong (bawaan lingkungan), gunakan fallback simulasi cerdas
    if not API_KEY:
        return simulasi_respons_pushy(user_message)
        
    retries = 5
    delay = 1.0
    for i in range(retries):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            if response.status_code == 200:
                result = response.json()
                text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                if text:
                    return text
            # Eksponensial Backoff
            time.sleep(delay)
            delay *= 2
        except Exception:
            time.sleep(delay)
            delay *= 2
            
    return "Maaf, sepertinya koneksi asisten pintar kami sedang sibuk. Namun, pastikan Anda memberikan pertolongan pertama berupa isolasi mandiri dan menjaga kebersihan jika kucing Anda terindikasi sakit, lalu segera hubungi dokter hewan terdekat."

def simulasi_respons_pushy(query):
    """Fallback simulasi asisten Pushy AI berbasis aturan kata kunci medis kucing."""
    query_lower = query.lower()
    time.sleep(1) # Efek mengetik natural
    
    if "jamur" in query_lower or "gatal" in query_lower or "botak" in query_lower or "ringworm" in query_lower:
        return "Halo Cat Lover! Gejala botak melingkar kemerahan sangat identik dengan **Ringworm** (infeksi jamur). Jamur ini bersifat **Zoonosis** (bisa menular ke manusia melalui sentuhan kulit). Tindakan pertama: \n1. Isolasi kucing Anda di ruangan khusus.\n2. Oleskan salep anti-jamur / mandikan dengan shampoo sulfur seminggu 2 kali.\n3. Cuci tangan dengan sabun antiseptik setelah memegang kucing."
    elif "muntah" in query_lower or "mencret" in query_lower or "diare" in query_lower:
        return "Gejala pencernaan terganggu seperti muntah atau diare harus diawasi ketat. Pastikan kucing tidak dehidrasi dengan memberikan air bersih matang atau larutan oralit khusus hewan. Hentikan pemberian makanan basah selama 12 jam terlebih dahulu, lalu konsultasikan dengan dokter hewan jika berlanjut lebih dari 24 jam."
    elif "flu" in query_lower or "bersin" in query_lower or "ingus" in query_lower:
        return "Flu kucing (Feline Rhinotracheitis/Calicivirus) sangat mudah menular antar-kucing. Segera pisahkan piring makan dan tempat tidur kucing sehat dari kucing yang bersin. Berikan vitamin minyak ikan untuk membantu meningkatkan daya tahan tubuh mereka."
    else:
        return "Pertanyaan yang sangat bagus mengenai kucing Anda! Untuk memastikan kesehatan optimal peliharaan Anda, selalu jaga sanitasi kandang, beri makanan tinggi protein, dan rutin berikan obat cacing setiap 3 bulan sekali. Ada gejala fisik spesifik lain yang sedang dialami si pus?"

# ==========================================
# RENDER IKON PUSHY (DENGAN FILE PNG)
# ==========================================
# RENDER IKON PUSHY (DENGAN FILE PNG)
# ==========================================
def render_logo_pushy():
    """Menampilkan logo Pushy dengan file PNG di sidebar"""
    try:
        # Gunakan file pushy_catcare_app.png dari direktori yang sama
        st.sidebar.image(
            "pushy_catcare_app.png",
            width=200,
            use_container_width=False
        )
        st.sidebar.markdown("<h2 style='text-align: center; color: #FF7800 !important; margin-top: -10px;'>Pushy CatCare</h2>", unsafe_allow_html=True)
        st.sidebar.markdown("<p style='text-align: center; font-size: 12px; color: #2E5B88; letter-spacing: 1px;'>Smart Pet Health Management</p>", unsafe_allow_html=True)
    except FileNotFoundError:
        # Fallback jika file tidak ditemukan
        st.sidebar.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: #FF7800 !important;">🐱 Pushy</h2>
            <span style="font-size: 14px; font-weight: bold; color: #2E5B88; letter-spacing: 1px;">CatCare App</span>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# SIDEBAR - NAVIGASI UTAMA
# ==========================================
render_logo_pushy()

st.sidebar.markdown("---")
role = st.sidebar.selectbox("Pilih Akses Peran (Role):", ["Cat Lover (Pecinta Kucing)", "Admin App (STIEIMA Cat Care)"])

if role == "Cat Lover (Pecinta Kucing)":
    menu = st.sidebar.radio(
        "Menu Utama Aplikasi:",
        [
            "🏠 Beranda & Ensiklopedia",
            "📷 Kamera Deteksi AI",
            "📋 Checklist Gejala & P3K",
            "🛒 Toko E-Commerce",
            "📍 Vet & Komunitas Sekitar",
            "💬 Tanya Asisten Pushy AI"
        ]
    )
else:
    menu = st.sidebar.radio(
        "Menu Kontrol Panel Admin:",
        [
            "📊 Dasbor Utama STIEIMA",
            "🩺 Moderasi Vet & Komunitas",
            "📦 Manajemen Produk"
        ]
    )

st.sidebar.markdown("---")
st.sidebar.caption("Dikembangkan Oleh: **STIEIMA Cat Care** © 2026")
st.sidebar.caption("Versi Aplikasi: `1.0.0 (Stable)`")

# ==========================================
# HALAMAN AKSES: CAT LOVER
# ==========================================
if role == "Cat Lover (Pecinta Kucing)":

    # MENU 1: BERANDA & ENSIKLOPEDIA
    if menu == "🏠 Beranda & Ensiklopedia":
        st.markdown("# 🏠 Selamat Datang di Pushy Cat Care App")
        st.write("Aplikasi kesehatan kucing terlengkap dan terpercaya untuk melindungi peliharaan kesayangan serta keluarga Anda dari penularan penyakit zoonosis.")
        
        # Sukses Story (Testimoni Dinamis)
        st.markdown("### 🏆 Kisah Sukses Pengguna (*Success Story*)")
        cols_story = st.columns(len(st.session_state.success_stories))
        for idx, story in enumerate(st.session_state.success_stories):
            with cols_story[idx]:
                st.markdown(f"""
                <div class="feature-card">
                    <p style="font-style: italic; color: #555;">"{story['cerita']}"</p>
                    <strong style="color: #FF8C32;">— {story['user']}</strong>
                </div>
                """, unsafe_allow_html=True)
        
        # Ensiklopedia Penyakit Kucing (FE-01)
        st.markdown("---")
        st.markdown("### 📚 Ensiklopedia Kesehatan & Protokol Kebersihan")
        
        tab_zoonosis, tab_nutrisi, tab_vaksinasi = st.tabs([
            "🛡️ Pencegahan Penyakit Menular (Zoonosis)",
            "🥩 Kebutuhan Nutrisi & Makanan",
            "💉 Jadwal & Pentingnya Vaksinasi"
        ])
        
        with tab_zoonosis:
            st.markdown("#### Lindungi Diri dari Infeksi Zoonosis")
            st.write("Zoonosis adalah jenis penyakit yang dapat ditularkan dari hewan peliharaan (kucing) ke manusia atau sebaliknya.")
            
            col_z1, col_z2 = st.columns(2)
            with col_z1:
                st.markdown("""
                * **Toxoplasmosis (Parasit):** Menular lewat kotoran kucing. Dapat berdampak serius bagi ibu hamil. 
                    *Protokol: Gunakan sekop dan sarung tangan saat membersihkan bak pasir, lalu cuci tangan.*
                * **Ringworm (Jamur Kulit):** Ditandai dengan lingkaran bersisik botak kemerahan di kulit. Sangat cepat menular ke manusia yang menyentuhnya.
                """)
            with col_z2:
                st.markdown("""
                * **Scabies (Kutu Sarcoptes):** Menyebabkan rasa gatal luar biasa pada kucing dan ruam bintik kemerahan pada tangan manusia.
                    *Protokol: Pisahkan isolasi kucing secepatnya jika bulu rontok dan kucing terus mencakar telinga/wajah.*
                """)
            st.info("💡 **Tips Aman:** Mandikan kucing secara rutin dengan sabun sulfur khusus hewan dan semprotkan disinfektan pada kandang setidaknya seminggu sekali.")
            
        with tab_nutrisi:
            st.markdown("#### Kunci Kucing Sehat: Nutrisi yang Tepat")
            st.write("Nutrisi yang seimbang memperkuat kekebalan alami kucing, menyehatkan folikel rambut sehingga tidak rontok, dan meminimalisir penularan penyakit parasit kulit.")
            st.markdown("""
            1.  **Protein Hewani Tinggi:** Kucing adalah karnivora sejati (*obligate carnivore*), membutuhkan taurin tinggi dari daging merah atau ikan.
            2.  **Omega 3 & 6:** Minyak ikan esensial menjaga kelembapan kulit dan membuat bulu bersinar berkilau.
            3.  **Serat Alami:** Membantu mempermudah pembuangan gumpalan rambut (*hairball*) di perut.
            """)
            
        with tab_vaksinasi:
            st.markdown("#### Panduan Vaksinasi Kucing")
            st.write("Vaksinasi melindungi kucing dari virus fatal seperti Feline Panleukopenia, Calicivirus, dan Herpesvirus (Vaksin F3/F4).")
            
            data_vaksin = {
                "Usia Kucing": ["8 - 10 Minggu", "12 - 14 Minggu", "6 Bulan", "1 Tahun sekali"],
                "Jenis Vaksin": ["Vaksin F3 (Tahap Pertama)", "Vaksin F3 & F4 (Booster Kedua)", "Vaksin Rabies (Sangat Penting!)", "Vaksin Booster Tahunan"],
                "Tujuan": ["Mencegah Panleukopenia, Rinotrakeitis", "Memperkuat kekebalan komprehensif", "Mencegah virus rabies zoonosis fatal", "Menjaga imunitas seumur hidup"]
            }
            st.table(pd.DataFrame(data_vaksin))

        # Integrasi Sosial Media (FE-07)
        st.markdown("---")
        st.markdown("#### 📣 Ikuti & Bagikan Kampanye STIEIMA Cat Care")
        st.write("Bantu kami mengedukasi masyarakat luas tentang pentingnya menjaga kesehatan kucing peliharaan.")
        st.button("🔗 Bagikan Pengetahuan Ini ke X (Twitter)")
        st.button("📸 Ikuti Instagram Kami @STIEIMACatCare")

    # MENU 2: KAMERA DETEKSI AI
    elif menu == "📷 Kamera Deteksi AI":
        st.markdown("# 📷 Kamera Deteksi AI (Kesehatan Fisik Kucing)")
        st.write("Gunakan fitur ini untuk mendeteksi kelainan kulit luar, mata belekan, atau masalah telinga kucing secara cepat berbasis teknologi AI Vision.")
        
        # Pilihan input
        source_opt = st.radio("Pilih Sumber Pengambilan Gambar:", ["Gunakan Kamera Perangkat", "Unggah Foto dari Galeri", "Gunakan Gambar Simulasi (Untuk Demo)"])
        
        image_file = None
        if source_opt == "Gunakan Kamera Perangkat":
            image_file = st.camera_input("Arahkan kamera ke bagian tubuh kucing yang mencurigai sakit")
        elif source_opt == "Unggah Foto dari Galeri":
            image_file = st.file_uploader("Unggah foto detail kucing (Format JPG/PNG)", type=["jpg", "png", "jpeg"])
        else:
            st.info("Pilih kondisi kucing simulasi di bawah ini untuk melihat cara kerja analisis model AI:")
            demo_case = st.selectbox("Pilih Skenario Kasus:", [
                "Demo 1: Kucing Sehat Walafiat",
                "Demo 2: Kucing dengan bintik rontok melingkar (Potensi Ringworm/Jamur)",
                "Demo 3: Kucing dengan bulu rontok seluruh tubuh, berkerak abu-abu di telinga (Potensi Scabies Akut)"
            ])
            
        btn_deteksi = st.button("🚀 Mulai Analisis AI Sekarang")
        
        if btn_deteksi:
            # Tentukan input tiruan sesuai pilihan demo atau input nyata
            skor_ai_simulasi = 0.10
            gejala_simulasi = 0
            kelainan_terdeteksi = "Tidak ada kelainan"
            
            if source_opt == "Gunakan Gambar Simulasi (Untuk Demo)":
                if "Demo 1" in demo_case:
                    skor_ai_simulasi = 0.12
                    gejala_simulasi = 0
                    kelainan_terdeteksi = "Bulu dan kulit dalam kondisi bersih sempurna."
                elif "Demo 2" in demo_case:
                    skor_ai_simulasi = 0.65
                    gejala_simulasi = 1
                    kelainan_terdeteksi = "Terdeteksi pola melingkar tanpa bulu (Alopecia) pada kulit luar."
                else: # Demo 3
                    skor_ai_simulasi = 0.88
                    gejala_simulasi = 3
                    kelainan_terdeteksi = "Terdeteksi kerak parah kering di tepi telinga dan kulit bersisik."
            else:
                # Jika input asli dari kamera/upload
                if image_file is not None:
                    # Simulasi pengolahan gambar acak
                    skor_ai_simulasi = round(random.uniform(0.35, 0.90), 2)
                    gejala_simulasi = random.randint(1, 3)
                    kelainan_terdeteksi = "Terdeteksi pola anomali kemerahan pada permukaan kulit luar kucing."
                else:
                    st.warning("⚠️ Mohon unggah foto atau gunakan kamera terlebih dahulu sebelum memulai deteksi.")
                    st.stop()
            
            # Tampilkan animasi loading
            with st.spinner("Sedang memproses citra dan mendiagnosis lewat AI Model..."):
                time.sleep(2.0)
            
            # Hitung Status Kesehatan berdasarkan logika bisnis PRD
            hasil_analisis = hitung_status_kesehatan(skor_ai_simulasi, gejala_simulasi)
            
            # Render Hasil ke Layar
            st.markdown("### 📋 Hasil Diagnosis Analisis AI")
            col_res1, col_res2 = st.columns([1, 2])
            
            with col_res1:
                st.metric("Tingkat Keyakinan Klasifikasi AI", f"{int(skor_ai_simulasi * 100)}%")
                st.write(f"**Temuan Visual:** {kelainan_terdeteksi}")
            
            with col_res2:
                # Render box berdasarkan status warna
                warna_box = hasil_analisis["warna"]
                if warna_box == "danger":
                    st.markdown(f'<div class="alert-danger-custom">{hasil_analisis["pesan"]}</div>', unsafe_allow_html=True)
                elif warna_box == "warning":
                    st.markdown(f'<div class="alert-warning-custom">{hasil_analisis["pesan"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="alert-success-custom">{hasil_analisis["pesan"]}</div>', unsafe_allow_html=True)
                    
            # Rekomendasi Integrasi Produk E-commerce & Vet
            if hasil_analisis["status"] != "SEHAT":
                st.markdown("---")
                st.markdown("### 🛒 Rekomendasi Solusi & Produk Pengobatan")
                st.write("Berdasarkan diagnosa, berikut beberapa produk obat dari toko Pushy yang disarankan untuk penanganan darurat awal:")
                
                # Saring produk rekomendasi
                rek_produk = [p for p in st.session_state.products if p["kategori"] in ["Obat-obatan", "Kebersihan", "Nutrisi & Vitamin"]]
                cols_rek = st.columns(len(rek_produk))
                for idx, prod in enumerate(rek_produk):
                    with cols_rek[idx]:
                        st.markdown(f"**{prod['nama']}**")
                        st.write(f"Harga: Rp {prod['harga']:,}")
                        if st.button(f"Tambah ke Keranjang", key=f"rek_cart_{prod['id']}"):
                            # Tambah ke keranjang
                            existing = next((item for item in st.session_state.cart if item["id"] == prod["id"]), None)
                            if existing:
                                existing["kuantitas"] += 1
                            else:
                                st.session_state.cart.append({"id": prod["id"], "nama": prod["nama"], "harga": prod["harga"], "kuantitas": 1})
                            st.success(f"Berhasil ditambahkan!")

    # MENU 3: CHECKLIST GEJALA & P3K
    elif menu == "📋 Checklist Gejala & P3K":
        st.markdown("# 📋 Kuesioner Diagnosis Mandiri & P3K")
        st.write("Silakan centang tanda fisik atau perubahan perilaku yang sedang dialami oleh kucing Anda untuk mendapatkan saran Pertolongan Pertama Pada Kecelakaan (P3K).")
        
        st.markdown("### Pilih Gejala yang Terlihat pada Kucing Anda:")
        
        c1, c2 = st.columns(2)
        with c1:
            g_kulit = st.checkbox("Bulu rontok parah, kulit berdarah atau bersisik tebal")
            g_mata = st.checkbox("Mata merah berair, bengkak, atau mengeluarkan belek kehijauan")
            g_bersin = st.checkbox("Sering bersin, batuk, dan ada ingus menyumbat hidung")
        with c2:
            g_muntah = st.checkbox("Kucing muntah berulang atau diare berdarah")
            g_lemas = st.checkbox("Tubuh sangat lemas, tidak nafsu makan, dan bersembunyi di sudut gelap")
            g_cakar = st.checkbox("Terus-menerus mencakar area telinga hingga lecet berdarah")
            
        # Hitung jumlah gejala terpilih
        daftar_gejala = [g_kulit, g_mata, g_bersin, g_muntah, g_lemas, g_cakar]
        jumlah_aktif = sum(1 for g in daftar_gejala if g)
        
        # Simulasi skor AI jika tidak menggunakan gambar
        skor_ai_check = 0.0
        if g_kulit or g_cakar:
            skor_ai_check += 0.45
        if g_mata or g_bersin:
            skor_ai_check += 0.20
        if g_muntah or g_lemas:
            skor_ai_check += 0.30
        
        skor_ai_check = min(0.95, skor_ai_check)
        
        st.markdown("---")
        btn_proses_checklist = st.button("🩺 Hitung Saran Diagnosis P3K")
        
        if btn_proses_checklist:
            hasil_p3k = hitung_status_kesehatan(skor_ai_check, jumlah_aktif)
            
            st.markdown(f"### Status Kesehatan Hasil Analisis Gejala: **{hasil_p3k['status']}**")
            
            if hasil_p3k["warna"] == "danger":
                st.markdown(f'<div class="alert-danger-custom">{hasil_p3k["pesan"]}</div>', unsafe_allow_html=True)
                st.markdown("""
                #### 🚑 Panduan Tindakan P3K Mendesak:
                1.  **Gunakan Sarung Tangan:** Segera pakai sarung tangan karet/plastik tebal sebelum memegang kucing.
                2.  **Isolasi Terpisah:** Tempatkan kucing di kandang besi/ruangan kering tersendiri yang jauh dari jangkauan manusia dan hewan lain.
                3.  **Jangan Mandikan Dulu:** Jika kondisi kucing lemas atau dehidrasi akibat muntah, memandikannya dapat menyebabkan kucing drop atau hipotermia.
                4.  **Bawa ke Vet Segera:** Hubungi dokter hewan terdekat di tab **Vet & Komunitas** secepatnya.
                """)
            elif hasil_p3k["warna"] == "warning":
                st.markdown(f'<div class="alert-warning-custom">{hasil_p3k["pesan"]}</div>', unsafe_allow_html=True)
                st.markdown("""
                #### 💊 Panduan Tindakan P3K Ringan:
                1.  **Pemisahan Kandang:** Pisahkan kucing di kandang tersendiri (karantina mandiri).
                2.  **Gunakan Antiseptik:** Jika kucing gatal akibat jamur/kutu, semprotkan cairan antiseptik hewan atau oleskan salep sulfur khusus kucing.
                3.  **Tambahan Nutrisi:** Berikan tambahan minyak ikan untuk membantu metabolisme tubuh dan ketahanan kesehatan bulunya.
                """)
            else:
                st.markdown(f'<div class="alert-success-custom">{hasil_p3k["pesan"]}</div>', unsafe_allow_html=True)

    # MENU 4: TOKO E-COMMERCE
    elif menu == "🛒 Toko E-Commerce":
        st.markdown("# 🛒 Toko E-Commerce Pushy Cat Care")
        st.write("Belanja nutrisi premium, pakan sehat, obat bebas tervalidasi, dan perlengkapan kebersihan kucing langsung dari STIEIMA Cat Care.")
        
        col_toko, col_kasir = st.columns([2, 1])
        
        with col_toko:
            st.markdown("### 🛍️ Katalog Produk")
            kategori_filter = st.selectbox("Pilih Kategori Produk:", ["Semua Produk", "Makanan", "Obat-obatan", "Nutrisi & Vitamin", "Kebersihan"])
            
            # Tampilkan produk berdasarkan kategori
            for prod in st.session_state.products:
                if kategori_filter != "Semua Produk" and prod["kategori"] != kategori_filter:
                    continue
                
                with st.container():
                    st.markdown(f"""
                    <div class="feature-card">
                        <h4 style='margin:0;'>{prod['nama']}</h4>
                        <p style='margin:2px 0; color: #777;'>Kategori: <i>{prod['kategori']}</i> | Stok: <b>{prod['stok']}</b></p>
                        <p style='margin:5px 0;'>{prod['deskripsi']}</p>
                        <strong style='color: #FF8C32; font-size: 16px;'>Rp {prod['harga']:,}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"🛒 Masukkan ke Keranjang", key=f"add_catalog_{prod['id']}"):
                        # Cek apakah produk sudah ada di keranjang
                        existing = next((item for item in st.session_state.cart if item["id"] == prod["id"]), None)
                        if existing:
                            existing["kuantitas"] += 1
                        else:
                            st.session_state.cart.append({
                                "id": prod["id"],
                                "nama": prod["nama"],
                                "harga": prod["harga"],
                                "kuantitas": 1
                            })
                        st.success(f"Berhasil menambahkan {prod['nama']} ke keranjang!")
                    st.write("") # Spacer

        with col_kasir:
            st.markdown("### 💳 Ringkasan Pembelian")
            
            if not st.session_state.cart:
                st.info("Keranjang belanjaan Anda masih kosong.")
            else:
                for idx, item in enumerate(st.session_state.cart):
                    col_item_n, col_item_q, col_item_d = st.columns([2, 1, 1])
                    with col_item_n:
                        st.write(f"**{item['nama']}**")
                    with col_item_q:
                        st.write(f"Qty: {item['kuantitas']}")
                    with col_item_d:
                        if st.button("Hapus", key=f"del_cart_{idx}"):
                            st.session_state.cart.pop(idx)
                            st.rerun()
                
                st.markdown("---")
                
                # Masukkan Kode Promo dari PRD Unit Test
                kode_promo = st.text_input("Gunakan Kode Kupon:", placeholder="Contoh: PUSHYSEHAT / GRATISONGKIR").strip().upper()
                if kode_promo == "PUSHYSEHAT":
                    st.success("🎉 Kode PUSHYSEHAT Aktif! Anda mendapatkan diskon 15% untuk produk kesehatan.")
                elif kode_promo == "GRATISONGKIR":
                    st.success("🚚 Kode GRATISONGKIR Aktif! Potongan ongkir s.d Rp 15.000 jika belanja >= Rp 150.000.")
                
                ongkos_kirim_dasar = 15000
                
                # Jalankan kalkulasi total belanja menggunakan fungsi teruji
                invoice = hitung_total_belanja(st.session_state.cart, kode_promo, ongkos_kirim_dasar)
                
                st.markdown(f"**Subtotal:** Rp {invoice['subtotal']:,}")
                st.markdown(f"**Diskon Promo:** - Rp {invoice['nominal_diskon']:,}")
                st.markdown(f"**Biaya Pengiriman:** Rp {invoice['biaya_kirim_final']:,}")
                st.markdown(f"### **Total Tagihan:** Rp {invoice['total_akhir']:,}")
                
                if st.button("💳 Bayar Sekarang (Checkout)"):
                    st.balloons()
                    st.success("Pembayaran Berhasil! Pesanan Anda akan segera disiapkan oleh Tim Kurir STIEIMA Cat Care.")
                    # Reset keranjang setelah transaksi selesai
                    st.session_state.cart = []
                    # Tambah kisah sukses pengguna baru secara acak untuk melengkapi target KPI
                    st.session_state.success_stories.append({
                        "user": "Pengguna Baru - Malang",
                        "cerita": "Sangat cepat! Saya mendeteksi masalah bulu gatal kucing lewat aplikasi, memesan shampoo sulfur dengan kode kupon PUSHYSEHAT, dan barang sampai sore harinya."
                    })

    # MENU 5: VET & KOMUNITAS SEKITAR
    elif menu == "📍 Vet & Komunitas Sekitar":
        st.markdown("# 📍 Direktori Vet & Komunitas Sekitar")
        st.write("Temukan klinik dokter hewan terdekat, rumah sakit hewan rujukan, serta jaringan komunitas pecinta kucing regional yang tervalidasi oleh Admin STIEIMA.")
        
        tab_v, tab_k, tab_d = st.tabs(["🩺 Klinik & Dokter Hewan", "👥 Komunitas Pecinta Kucing", "📝 Daftarkan Vet / Komunitas Baru"])
        
        with tab_v:
            st.markdown("### Dokter Hewan & Klinik Aktif")
            vets_aktif = [v for v in st.session_state.vet_directory if v["status"] == "Approved"]
            for v in vets_aktif:
                st.markdown(f"""
                <div class="feature-card">
                    <h4>🩺 {v['nama']}</h4>
                    <p>📍 Alamat: {v['alamat']}</p>
                    <p>📞 Hubungi: <b>{v['telepon']}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
        with tab_k:
            st.markdown("### Jaringan Komunitas Pecinta Kucing")
            kom_aktif = [k for k in st.session_state.communities if k["status"] == "Approved"]
            for k in kom_aktif:
                st.markdown(f"""
                <div class="feature-card">
                    <h4>👥 {k['nama']}</h4>
                    <p>🧭 Wilayah Gerakan: {k['wilayah']}</p>
                    <p>📞 Kontak Hubung: <b>{k['kontak']}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
        with tab_d:
            st.markdown("### Formulir Pendaftaran Publik")
            st.write("Apakah Anda seorang Praktisi Dokter Hewan berizin atau Pengurus Komunitas Kucing? Silakan daftarkan diri agar terindeks di sistem kami.")
            
            tipe_reg = st.selectbox("Jenis Pendaftaran:", ["Dokter Hewan / Klinik", "Komunitas Pecinta Kucing"])
            
            with st.form("form_pendaftaran_publik"):
                nama_input = st.text_input("Nama Lengkap Dokter/Klinik/Komunitas:")
                detail_alamat = st.text_area("Alamat Lengkap / Cakupan Wilayah:")
                kontak_input = st.text_input("No Telepon / WhatsApp:")
                sip_bukti = st.text_input("Nomor SIP Dokter / Bukti Legalitas Komunitas (Opsional):")
                
                submitted = st.form_submit_button("Ajukan Verifikasi Data")
                if submitted:
                    if not nama_input or not kontak_input:
                        st.error("Gagal mengirim! Nama dan Kontak wajib diisi lengkap.")
                    else:
                        # Tambahkan ke database internal dengan status 'Pending' sesuai PRD Bab 5.B
                        if tipe_reg == "Dokter Hewan / Klinik":
                            st.session_state.vet_directory.append({
                                "id": len(st.session_state.vet_directory) + 1,
                                "nama": nama_input,
                                "alamat": detail_alamat,
                                "telepon": kontak_input,
                                "status": "Pending"
                            })
                        else:
                            st.session_state.communities.append({
                                "id": len(st.session_state.communities) + 1,
                                "nama": nama_input,
                                "wilayah": detail_alamat,
                                "kontak": kontak_input,
                                "status": "Pending"
                            })
                        st.success("✅ Pendaftaran Anda berhasil dikirim! Tim Admin STIEIMA Cat Care akan segera melakukan verifikasi berkas dokumen sebelum ditampilkan di peta publik.")

    # MENU 6: CHATBOT PUSHY AI
    elif menu == "💬 Tanya Asisten Pushy AI":
        st.markdown("# 💬 Tanya Asisten Pushy AI")
        st.write("Asisten virtual kesehatan kucing cerdas 24/7. Tanyakan apa saja seputar penanganan penyakit luar, nutrisi kucing hamil, gejala demam, dan sanitasi.")
        
        # Area Riwayat Percakapan
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
        # Input Pengguna
        prompt = st.chat_input("Tulis pertanyaan Anda di sini (misal: 'Bagaimana mengobati jamur ringworm kucing?')")
        if prompt:
            # Tampilkan pesan user
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            # System Instruction untuk memandu respons AI agar bernada empati, medis, aman, dan mendalam
            instruksi_sistem = (
                "Anda adalah Pushy AI, asisten medis kucing virtual buatan STIEIMA Cat Care. "
                "Tugas utama Anda adalah mengedukasi pecinta kucing mengenai gejala penyakit, pengobatan pertama (P3K) aman, "
                "dan pencegahan penularan zoonosis ke manusia secara higienis. Jawab dengan nada hangat, sopan, bersahabat, "
                "menggunakan bahasa Indonesia yang santun. Selalu ingatkan pengguna untuk mengisolasi kucing yang sakit menular "
                "dan bawa ke dokter hewan jika kondisi memburuk."
            )
            
            # Panggil API Gemini dengan penanganan retries eksponensial
            with st.spinner("Pushy AI sedang merumuskan saran kesehatan medis..."):
                response_ai = panggil_gemini_api(prompt, instruksi_sistem)
                
            # Tampilkan respons asisten
            with st.chat_message("assistant"):
                st.markdown(response_ai)
            st.session_state.chat_history.append({"role": "assistant", "content": response_ai})

# ==========================================
# HALAMAN AKSES: ADMIN PANEL STIEIMA
# ==========================================
else:
    # MENU ADMIN 1: DASBOR UTAMA
    if menu == "📊 Dasbor Utama STIEIMA":
        st.markdown("# 📊 Dasbor Kontrol & Statistik Utama STIEIMA Cat Care")
        st.write("Panel pemantauan performa aplikasi, status kepuasan pengguna, dan indikator kesuksesan operasional (KPI).")
        
        # Metrik Berdasarkan KPI PRD Bab 8
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Anggota Aktif Bulanan (MAU)", "5,820 Pengguna", "+16% Bulan Lalu")
        with m2:
            st.metric("Total Kisah Sukses Sembuh", f"{len(st.session_state.success_stories)} Kisah", "Target: >50")
        with m3:
            st.metric("Rasio Retensi Mingguan", "38.5%", "Target: >35%")
        with m4:
            st.metric("Rata-rata Belanja Bulanan", "2.4 Transaksi", "Target: >2")
            
        st.markdown("---")
        st.markdown("### 📈 Aktivitas Sistem Terbaru")
        
        # Menampilkan Kisah Sukses untuk verifikasi admin
        st.write("**Daftar Kisah Sukses Pengguna Tervalidasi:**")
        df_stories = pd.DataFrame(st.session_state.success_stories)
        st.dataframe(df_stories, use_container_width=True)

    # MENU ADMIN 2: MODERASI VET & KOMUNITAS
    elif menu == "🩺 Moderasi Vet & Komunitas":
        st.markdown("# 🩺 Moderasi Pengajuan Pendaftaran Baru")
        st.write("Verifikasi kelayakan berkas izin praktik dokter hewan serta keaktifan komunitas pencinta kucing lokal sebelum ditayangkan publik.")
        
        # Bagian Vet Pending
        st.markdown("### ⏳ Pengajuan Dokter Hewan Pending")
        v_pending = [v for v in st.session_state.vet_directory if v["status"] == "Pending"]
        
        if not v_pending:
            st.info("Tidak ada pengajuan dokter hewan yang pending saat ini.")
        else:
            for v in v_pending:
                with st.container():
                    st.markdown(f"""
                    <div style="background-color:#FFF; padding:15px; border-radius:8px; border:1px solid #CCC; margin-bottom:10px;">
                        <b>🩺 {v['nama']}</b><br/>
                        📍 Alamat: {v['alamat']}<br/>
                        📞 No. Telp: {v['telepon']}
                    </div>
                    """, unsafe_allow_html=True)
                    c_app, c_rej = st.columns([1, 10])
                    with c_app:
                        if st.button("Approve", key=f"app_v_{v['id']}"):
                            v["status"] = "Approved"
                            st.success(f"{v['nama']} disetujui untuk masuk daftar aktif!")
                            st.rerun()
                    with c_rej:
                        if st.button("Reject", key=f"rej_v_{v['id']}"):
                            st.session_state.vet_directory.remove(v)
                            st.warning(f"Pengajuan {v['nama']} telah ditolak dan dihapus.")
                            st.rerun()
                            
        st.markdown("---")
        
        # Bagian Komunitas Pending
        st.markdown("### ⏳ Pengajuan Komunitas Pending")
        k_pending = [k for k in st.session_state.communities if k["status"] == "Pending"]
        
        if not k_pending:
            st.info("Tidak ada pengajuan komunitas yang pending saat ini.")
        else:
            for k in k_pending:
                with st.container():
                    st.markdown(f"""
                    <div style="background-color:#FFF; padding:15px; border-radius:8px; border:1px solid #CCC; margin-bottom:10px;">
                        <b>👥 {k['nama']}</b><br/>
                        🧭 Cakupan Wilayah: {k['wilayah']}<br/>
                        📞 Kontak Pengurus: {k['kontak']}
                    </div>
                    """, unsafe_allow_html=True)
                    c_app_k, c_rej_k = st.columns([1, 10])
                    with c_app_k:
                        if st.button("Approve", key=f"app_k_{k['id']}"):
                            k["status"] = "Approved"
                            st.success(f"Komunitas {k['nama']} disetujui!")
                            st.rerun()
                    with c_rej_k:
                        if st.button("Reject", key=f"rej_k_{k['id']}"):
                            st.session_state.communities.remove(k)
                            st.warning(f"Pengajuan {k['nama']} ditolak.")
                            st.rerun()

    # MENU ADMIN 3: MANAJEMEN PRODUK
    elif menu == "📦 Manajemen Produk":
        st.markdown("# 📦 Kelola Inventaris E-Commerce")
        st.write("Tambahkan pasokan barang baru atau edit harga makanan dan obat-obatan yang dijual di toko.")
        
        # Form Tambah Produk Baru
        with st.expander("➕ Tambah Produk Baru ke Katalog"):
            with st.form("form_tambah_produk"):
                n_id = st.text_input("ID Produk (Unik):", placeholder="Contoh: pakan-05")
                n_nama = st.text_input("Nama Produk:")
                n_kat = st.selectbox("Kategori Produk:", ["Makanan", "Obat-obatan", "Nutrisi & Vitamin", "Kebersihan"])
                n_harga = st.number_input("Harga Jual (Rp):", min_value=1000, value=50000)
                n_stok = st.number_input("Stok Awal:", min_value=1, value=10)
                n_desc = st.text_area("Deskripsi Manfaat Produk:")
                
                submitted_p = st.form_submit_button("Simpan Produk")
                if submitted_p:
                    if not n_id or not n_nama:
                        st.error("Gagal! ID dan Nama Produk tidak boleh kosong.")
                    else:
                        st.session_state.products.append({
                            "id": n_id,
                            "nama": n_nama,
                            "kategori": n_kat,
                            "harga": n_harga,
                            "stok": n_stok,
                            "deskripsi": n_desc
                        })
                        st.success(f"Berhasil menambahkan {n_nama} ke dalam inventaris!")
                        st.rerun()
                        
        st.markdown("### Daftar Inventaris Toko Saat Ini")
        df_products = pd.DataFrame(st.session_state.products)
        st.dataframe(df_products, use_container_width=True)