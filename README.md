# pushy_cat_care_app
Aplikasi komunitas untuk memelihara kucing dengan lebih baik
🐱 Pushy Cat Care App
adalah aplikasi manajemen perawatan kucing cerdas yang dikembangkan oleh STIEIMA Cat Care. Aplikasi ini dirancang khusus untuk membantu para pecinta kucing (Cat Lovers) mendeteksi dini masalah kesehatan fisik kucing, memberikan panduan Pertolongan Pertama Pada Kecelakaan (P3K) guna mencegah risiko penyakit menular (zoonosis), berbelanja kebutuhan nutrisi/obat, serta terhubung dengan ekosistem dokter hewan dan komunitas terdekat.
Aplikasi ini dibangun menggunakan framework Python Streamlit dengan visualisasi interaktif, simulasi AI Vision, kalkulator transaksi e-commerce dinamis, serta integrasi asisten cerdas berbasis Gemini API.
🌟 Fitur Utama
Aplikasi ini menyediakan dua ruang akses peran (Role Access):
1. 🐱 Peran: Cat Lover (Pecinta Kucing)
🏠 Beranda & Ensiklopedia: Pusat edukasi interaktif mengenai pencegahan penyakit zoonosis (seperti Toxoplasmosis, Ringworm, Scabies), panduan nutrisi seimbang, serta tabel jadwal vaksinasi lengkap.
📷 Kamera Deteksi AI: Simulasi analisis citra medis fisik luar kucing (kulit, telinga, mata) untuk mengklasifikasikan tingkat keparahan kondisi kucing (Sehat, Perlu Perhatian, atau Bahaya) secara instan.
📋 Checklist Gejala & P3K: Kuesioner diagnosis mandiri berbasis gejala fisik yang langsung memberikan rekomendasi tindakan darurat P3K yang aman untuk pemilik dan kucing.
🛒 Toko E-Commerce: Katalog produk makanan, obat-obatan, nutrisi, dan kebersihan dengan integrasi sistem kasir otomatis yang mendukung penggunaan kode kupon promo:
PUSHYSEHAT (Diskon 15% untuk produk kesehatan).
GRATISONGKIR (Potongan biaya kirim hingga Rp 15.000 untuk belanja di atas Rp 150.000).
📍 Vet & Komunitas Sekitar: Direktori aktif dokter hewan, klinik, dan komunitas pecinta kucing sekitar. Pengguna juga dapat mengajukan pendaftaran klinik/komunitas baru melalui formulir publik.
💬 Tanya Asisten Pushy AI: Chatbot asisten medis virtual 24/7 yang responsif, ditenagai oleh integrasi API LLM Gemini (gemini-2.5-flash-preview-09-2025) dengan algoritma retries eksponensial (hingga 5 kali) serta sistem simulasi cerdas sebagai fallback jika kunci API tidak terpasang.
2. 📊 Peran: Admin App (STIEIMA Cat Care)
📊 Dasbor Utama STIEIMA: Memantau metrik kesuksesan operasional (KPI) secara real-time, seperti Anggota Aktif Bulanan (MAU), total kisah sukses sembuh, rasio retensi mingguan, dan rata-rata transaksi.
🩺 Moderasi Vet & Komunitas: Menyetujui (Approve) atau Menolak (Reject) berkas data pengajuan klinik dokter hewan dan komunitas baru yang didaftarkan oleh publik.
📦 Manajemen Produk: Mengelola ketersediaan inventaris e-commerce dengan menambahkan produk baru ke katalog internal aplikasi secara instan.
🛠️ Prasyarat & Instalasi
Sebelum menjalankan aplikasi, pastikan Anda telah menginstal Python (versi 3.8 ke atas) di komputer Anda.
1. Klon Repositori
git clone [https://github.com/nasriaw/pushy-cat-care-app.git]

2. Instalasi Dependensi (Library)
Instal seluruh paket dependensi Python yang dibutuhkan melalui pip:
pip install streamlit pandas requests


🚀 Cara Menjalankan Aplikasi
Jalankan server lokal Streamlit Anda dengan mengeksekusi perintah berikut di terminal:
streamlit run pushy_cat_care_app.py


Setelah perintah dijalankan, peramban (web browser) Anda akan otomatis terbuka dan mengarah ke alamat lokal aplikasi: http://localhost:8501.
🔑 Konfigurasi API Chatbot (Gemini API)
Aplikasi ini menggunakan API model AI non-streaming gemini-2.5-flash-preview-09-2025 untuk menghasilkan respons konsultasi kesehatan kucing yang akurat pada menu Tanya Asisten Pushy AI.
Secara bawaan, jika kunci API dikosongkan, chatbot akan berjalan menggunakan Simulasi Respons Cerdas lokal berbasis deteksi kata kunci medis umum kucing (Ringworm, Scabies, Flu, Muntah, dll).
Untuk mengaktifkan kecerdasan penuh model AI Gemini:
Buka berkas pushy_cat_care_app.py.
Temukan variabel API_KEY di bagian konfigurasi halaman:
# Masukkan API Key Gemini Anda di sini
API_KEY = "ISI_DENGAN_API_KEY_GEMINI_ANDA"


Simpan berkas dan muat ulang halaman Streamlit Anda.
🧪 Pengujian Unit (Unit Testing)
Sesuai dengan cetak biru PRD, logika bisnis inti dilindungi oleh skenario pengujian unit (Unit Test) terstandarisasi guna memastikan keandalan fungsi komputasi.
A. Pengujian Backend: Klasifikasi AI Kesehatan Kucing (Python/PyTest)
Berfungsi menguji kebenaran penentuan status bahaya medis kucing dan rekomendasi isolasi penularan zoonosis.
File Uji: tests/test_health_classifier.py
Cara Menjalankan:
pip install pytest
pytest tests/test_health_classifier.py


B. Pengujian Frontend: Modul Kasir E-Commerce (JavaScript/Jest)
Menguji keandalan logika pemotongan harga kupon, pemotongan biaya kirim, akumulasi subtotal belanjaan, dan pencegahan error masukan data bukan array.
File Uji: tests/ecommerceCart.test.js
Cara Menjalankan:
npm install --save-dev jest
npm test tests/ecommerceCart.test.js


📂 Struktur Berkas Proyek
pushy-cat-care-app/
│
├── pushy_cat_care_app.py      # Berkas Utama Aplikasi Streamlit
├── README.md                  # Dokumentasi Proyek (Berkas ini)
│
└── tests/
    ├── test_health_classifier.py  # Unit Test Logika Kesehatan (PyTest)
    └── ecommerceCart.test.js      # Unit Test Logika Kasir (Jest)


📄 Kontribusi
Proyek ini dikembangkan secara kolaboratif oleh tim akademik dan praktisi dari STIEIMA Cat Care. Apabila Anda ingin berkontribusi dalam pengembangan model klasifikasi citra AI atau penguatan fitur logistik e-commerce, silakan hubungi tim administrator kampus STIEIMA Malang.
