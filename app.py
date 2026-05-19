from flask import Flask, render_template, request, abort
from services import mealdb_api

app = Flask(__name__)

# Default kategori yang ditampilkan di halaman utama
DEFAULT_CATEGORY = "Seafood"


@app.context_processor
def inject_globals():
    """
    Sediakan data global yang dibutuhkan oleh hampir semua template
    (terutama navigasi: daftar kategori).
    """
    return {
        "nav_categories": mealdb_api.get_categories()[:8],  # 8 kategori populer di nav
        "site_name": "ResepKita",
    }


# ROUTES

@app.route("/")
def index():
    """
    Halaman utama. Menampilkan minimal 10 resep dari kategori default
    (Seafood) — TheMealDB mengembalikan ±25-30 resep per kategori.
    Mendukung query string:
        ?sort=asc | desc       — sorting berdasarkan nama
    """
    sort_order = request.args.get("sort", "asc")
    meals = mealdb_api.filter_by_category(DEFAULT_CATEGORY)
    meals = mealdb_api.sort_meals(meals, order=sort_order)

    # Ambil 1 meal random untuk hero section
    featured = mealdb_api.get_random_meal()

    return render_template(
        "index.html",
        meals=meals,
        category=DEFAULT_CATEGORY,
        sort_order=sort_order,
        featured=featured,
        total=len(meals),
    )


@app.route("/category/<name>")
def category(name):
    """Tampilkan semua resep dalam satu kategori."""
    sort_order = request.args.get("sort", "asc")
    meals = mealdb_api.filter_by_category(name)
    meals = mealdb_api.sort_meals(meals, order=sort_order)

    return render_template(
        "category.html",
        meals=meals,
        category=name,
        sort_order=sort_order,
        total=len(meals),
    )


@app.route("/area/<name>")
def area(name):
    """Tampilkan semua resep dari satu area/negara asal."""
    sort_order = request.args.get("sort", "asc")
    meals = mealdb_api.filter_by_area(name)
    meals = mealdb_api.sort_meals(meals, order=sort_order)

    return render_template(
        "area.html",
        meals=meals,
        area=name,
        sort_order=sort_order,
        total=len(meals),
    )


@app.route("/search")
def search():
    """
    Fitur pencarian — Soal 3.
    Mendukung pencarian partial-match berdasarkan nama resep.
    """
    query = request.args.get("q", "").strip()
    sort_order = request.args.get("sort", "asc")

    meals = []
    if query:
        meals = mealdb_api.search_by_name(query)
        meals = mealdb_api.sort_meals(meals, order=sort_order)

    return render_template(
        "search.html",
        meals=meals,
        query=query,
        sort_order=sort_order,
        total=len(meals),
    )


@app.route("/meal/<meal_id>")
def meal_detail(meal_id):
    """
    Halaman detail resep — Soal 3 (fitur "Menampilkan detail data").
    Menampilkan bahan, takaran, instruksi, video tutorial, dll.
    """
    meal = mealdb_api.get_meal_detail(meal_id)
    if not meal:
        abort(404)

    ingredients = mealdb_api.extract_ingredients(meal)
    return render_template("detail.html", meal=meal, ingredients=ingredients)


@app.route("/areas")
def areas():
    """Halaman daftar semua area/negara asal masakan."""
    all_areas = mealdb_api.list_areas()
    return render_template("areas.html", areas=all_areas)


@app.route("/about")
def about():
    """
    Halaman penjelasan — Soal 5.
    Berisi penjelasan tema, API yang dipakai, cara kerja, fitur, insight.
    """
    return render_template("about.html")



# ERROR HANDLERS

@app.errorhandler(404)
def not_found(_):
    return render_template("error.html", code=404,
                           message="Halaman atau resep yang Anda cari tidak ditemukan."), 404


@app.errorhandler(500)
def server_error(_):
    return render_template("error.html", code=500,
                           message="Terjadi kesalahan di server. Coba lagi nanti."), 500



# ENTRY POINT

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
