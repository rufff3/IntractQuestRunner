==============================================
 README - Script Otomatisasi Verifikasi Intract
==============================================

📌 DESKRIPSI
------------
Script ini digunakan untuk memverifikasi tugas di situs quest.intract.io secara otomatis **hanya untuk kasus ketika API dalam kondisi mati**. 
Script ini bekerja dengan melakukan klik langsung terhadap elemen tombol "Verify", **tidak untuk menyelesaikan tugas kuis (quiz)** karena tidak didukung dalam mode ini.

Fungsi utama:
- Membaca cookies dari file `cookiesintract.txt`
- Login otomatis ke akun menggunakan cookies
- Membuka link quest yang diberikan
- Menekan tombol "See More" (jika ada)
- Memverifikasi semua tugas yang bisa diverifikasi
- Mendukung banyak akun (multi-cookies dalam satu file)

📂 STRUKTUR COOKIE
------------------
File cookie bernama `cookiesintract.txt` harus berisi satu atau lebih blok JSON cookies, misalnya:
[{{"name": "cookie_name", "value": "cookie_value", ...}}][{{"name": "cookie_name", "value": "cookie_value", ...}}]
Script akan otomatis memisahkan blok `[...][...]` menjadi akun yang berbeda, cookies satu dan lainnya cukup enter dibawahnya dan tempel untuk memisahkan tiap cookiesnya.

⚙️ CARA PENGGUNAAN
-------------------
1. Siapkan file cookies `cookiesintract.txt` di folder yang sama dengan script.
2. Jalankan script dengan perintah:

   python namascriptkamu.py

3. Masukkan link quest satu per satu, misalnya:

   https://quest.intract.io/campaign/abc123
   https://quest.intract.io/campaign/xyz789

4. Jika sudah selesai memasukkan link, ketik:

   selesai

5. Script akan:
   - Login dengan akun pertama
   - Membuka setiap link quest
   - Klik semua tombol "See More" dan "Verify"
   - Lanjut ke akun berikutnya setelah jeda 10 detik

📌 CATATAN PENTING
-------------------
- Script ini hanya dapat digunakan untuk **verifikasi manual via UI**, bukan penyelesaian tugas kuis atau tugas dengan API aktif.
- Pastikan semua cookies valid dan belum kadaluarsa.
- Jika terjadi error saat klik atau load halaman, script tetap akan melanjutkan ke akun berikutnya.

👨‍💻 KOMPONEN UTAMA
-------------------
- `load_cookies_from_file`: Membaca dan parsing cookies dari file
- `inject_cookies`: Menyuntikkan cookies ke sesi browser
- `shortcut_verification`: Klik semua tombol "See More" dan "Verify"
- `setup_driver`: Mengatur ChromeDriver headless
- `main`: Fungsi utama loop akun dan quest

✉️ KONTAK
---------
Script ini dibuat untuk keperluan pribadi atau riset automasi. Gunakan dengan bijak dan jangan melanggar ToS situs.
# IntractQuestRunner
