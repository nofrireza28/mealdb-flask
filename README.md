# ResepKita 🍽️

Website penjelajah resep masakan dari seluruh dunia, dibangun dengan **Python Flask** dan terintegrasi dengan API publik **[TheMealDB](https://www.themealdb.com/api.php)**.

> Project ini dibuat untuk memenuhi Ujian Tengah Semester (UTS) mata kuliah **Pemrograman Back End**.

---

## 📋 Fitur

- ✅ Integrasi dengan TheMealDB Public API
- ✅ Menampilkan 25+ resep di halaman utama (dari kategori populer)
- ✅ **Pencarian resep** berdasarkan nama (partial match)
- ✅ **Filter resep** berdasarkan kategori (Seafood, Beef, Vegetarian, dll)
- ✅ **Filter resep** berdasarkan negara asal (Italian, Japanese, Indonesian, dll)
- ✅ **Sorting** A→Z / Z→A
- ✅ **Halaman detail resep** dengan: bahan + takaran, instruksi memasak, link video YouTube
- ✅ "Resep pilihan hari ini" — featured random meal di beranda
- ✅ UI responsive (desktop & mobile)
- ✅ Halaman "Tentang" yang menjelaskan tema, API, cara kerja, dan insight
- ✅ Custom error pages (404, 500)

---

## 🛠️ Tech Stack

| Komponen | Teknologi |
|----------|-----------|
| Backend | Python 3.10+, Flask 3.x |
| HTTP Client | requests |
| Template | Jinja2 (built-in Flask) |
| Frontend | HTML5, CSS3 (vanilla), JavaScript (vanilla) |
| Data Source | TheMealDB API |

---

## 🚀 Cara Menjalankan

### 1. Pastikan Python sudah terinstall
```bash
python --version   # Minimal Python 3.10
```

### 2. Buat virtual environment (opsional tapi disarankan)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependency
```bash
pip install -r requirements.txt
```

### 4. Jalankan aplikasi
```bash
python app.py
```

### 5. Buka browser
```
http://localhost:5000
```

---

## 📁 Struktur Project

```
mealdb-flask/
├── app.py                      # Entry point Flask + routes
├── requirements.txt            # Dependency Python
├── README.md
├── services/
│   ├── __init__.py
│   └── mealdb_api.py           # Service layer (komunikasi ke TheMealDB)
├── templates/
│   ├── base.html               # Layout dasar (nav + footer)
│   ├── _macros.html            # Komponen reusable
│   ├── index.html              # Beranda
│   ├── category.html           # Filter per kategori
│   ├── area.html               # Filter per negara
│   ├── areas.html              # Daftar semua negara
│   ├── search.html             # Hasil pencarian
│   ├── detail.html             # Detail resep
│   ├── about.html              # Halaman tentang
│   └── error.html              # 404 / 500
├── static/
│   ├── css/style.css           # Stylesheet utama
│   └── js/main.js              # Interaksi ringan
└── docs/
    └── Dokumentasi.pdf         # Dokumentasi PDF
```

---

## 🌐 Routes

| Method | Path | Deskripsi |
|--------|------|-----------|
| GET | `/` | Beranda — featured + daftar resep kategori Seafood |
| GET | `/category/<name>` | Daftar resep per kategori |
| GET | `/area/<name>` | Daftar resep per negara asal |
| GET | `/areas` | Daftar semua negara |
| GET | `/search?q=<query>` | Pencarian resep |
| GET | `/meal/<id>` | Detail satu resep |
| GET | `/about` | Halaman tentang website |

Semua list endpoint juga mendukung query string `?sort=asc` atau `?sort=desc`.

---

## 🧩 API Endpoints yang Digunakan

Base URL: `https://www.themealdb.com/api/json/v1/1`

- `GET /categories.php` — daftar kategori (+ thumbnail)
- `GET /list.php?a=list` — daftar area/negara
- `GET /filter.php?c=<category>` — meals per kategori
- `GET /filter.php?a=<area>` — meals per area
- `GET /search.php?s=<query>` — pencarian by nama
- `GET /lookup.php?i=<id>` — detail meal by ID
- `GET /random.php` — meal random

---


## 📜 Lisensi

Project ini dibuat untuk keperluan akademis. Data resep merupakan milik TheMealDB.
