# Telegram Bots (2 Bots in 1)

## 📌 Penjelasan
- **main.py** → entry point, menerima command dari Telegram.  
- **bot.py** → bot 1.  
- **rug.py** → bot 2.  
- **pyTelegramBotAPI** → library utama untuk bot Telegram.  
- **requests** → untuk API call / HTTP request.  

> Kedua bot dijalankan **bersamaan 24/7** via main.py, tidak perlu dijalankan terpisah.

## 🛠️ Cara Setup
1. Buat file **requirements.txt** di folder project (sama level dengan main.py).  
2. Isi dengan daftar library di atas.  
3. Push ke GitHub.  
4. Deploy ke **Render worker** → Start Command:  