"""
TheMealDB API Service Layer
----------------------------
Modul ini bertanggung jawab untuk semua komunikasi ke API publik TheMealDB.
Memisahkan logika pemanggilan API dari route Flask agar lebih mudah dipelihara
dan dites.

Dokumentasi API: https://www.themealdb.com/api.php
"""

import requests
from typing import List, Dict, Optional

BASE_URL = "https://www.themealdb.com/api/json/v1/1"
TIMEOUT = 10  # detik


def _get(endpoint: str, params: Optional[Dict] = None) -> Dict:
    """
    Helper internal untuk GET request ke TheMealDB.
    Mengembalikan dict hasil parsing JSON. Bila gagal, kembalikan dict kosong
    agar aplikasi tidak crash dan tampilan tetap aman.
    """
    try:
        url = f"{BASE_URL}/{endpoint}"
        response = requests.get(url, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json() or {}
    except (requests.RequestException, ValueError) as exc:
        print(f"[MealDB API Error] {exc}")
        return {}

def get_categories() -> List[Dict]:
    """Ambil seluruh kategori makanan beserta thumbnail dan deskripsi."""
    data = _get("categories.php")
    return data.get("categories", []) or []

def list_areas() -> List[str]:
    """Ambil daftar nama area/negara asal masakan (string saja)."""
    data = _get("list.php", {"a": "list"})
    meals = data.get("meals", []) or []
    return [m["strArea"] for m in meals if m.get("strArea")]

def filter_by_category(category: str) -> List[Dict]:
    """
    Ambil daftar meals berdasarkan kategori.
    Response hanya berisi field dasar: idMeal, strMeal, strMealThumb.
    """
    data = _get("filter.php", {"c": category})
    return data.get("meals", []) or []

def filter_by_area(area: str) -> List[Dict]:
    """Ambil daftar meals berdasarkan area/negara asal."""
    data = _get("filter.php", {"a": area})
    return data.get("meals", []) or []

def search_by_name(query: str) -> List[Dict]:
    """
    Cari meal berdasarkan nama (partial match).
    Response berisi field lengkap untuk setiap meal yang cocok.
    """
    if not query or not query.strip():
        return []
    data = _get("search.php", {"s": query.strip()})
    return data.get("meals", []) or []

def get_meal_detail(meal_id: str) -> Optional[Dict]:
    """Ambil detail lengkap satu meal berdasarkan ID."""
    data = _get("lookup.php", {"i": meal_id})
    meals = data.get("meals", []) or []
    return meals[0] if meals else None

def get_random_meal() -> Optional[Dict]:
    """Ambil satu meal random — fitur tambahan untuk halaman utama."""
    data = _get("random.php")
    meals = data.get("meals", []) or []
    return meals[0] if meals else None

def extract_ingredients(meal: Dict) -> List[Dict[str, str]]:
    """
    Helper untuk mengubah struktur ingredient TheMealDB yang aneh
    (strIngredient1..strIngredient20 + strMeasure1..strMeasure20)
    menjadi list dict yang rapi: [{"name": ..., "measure": ...}, ...].
    """
    ingredients = []
    for i in range(1, 21):
        name = (meal.get(f"strIngredient{i}") or "").strip()
        measure = (meal.get(f"strMeasure{i}") or "").strip()
        if name:
            ingredients.append({"name": name, "measure": measure})
    return ingredients

def sort_meals(meals: List[Dict], order: str = "asc") -> List[Dict]:
    """Urutkan list meals berdasarkan nama (ascending/descending)."""
    reverse = order == "desc"
    return sorted(meals, key=lambda m: (m.get("strMeal") or "").lower(), reverse=reverse)
