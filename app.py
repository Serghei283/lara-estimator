from flask import Flask, render_template, request

app = Flask(__name__)

# --- БАЗОВЫЕ цены квартир по районам (евро/м²) ---
DISTRICT_PRICES = {
    "Centru": 1200,
    "Telecentru": 950,
    "Ciocana": 800,
    "Buiucani": 950,
    "Posta Veche": 850,
    "Durlești": 820,
    "Botanica": 1000,
    "Sculeni": 900,
    "Râșcani": 950,
    "Aeroport": 750
}

# --- Коэффициенты ремонта ---
REPAIR_COEFFICIENTS = {
    "Variantă sură": 0.75,
    "Variantă albă": 0.85,
    "Reparație cosmetică": 0.95,
    "Euroreparație": 1.15
}

# --- Коэффициенты по типу здания ---
BUILDING_COEFFICIENTS = {
    "Beton": 0.95,
    "Beton celular": 0.90,
    "Bloc": 0.85,
    "Combinat": 0.88,
    "Cotileț": 0.92,
    "Cărămidă": 1.05,
    "Lemn": 0.80,
    "Monolit": 1.10,
    "Panou": 0.82
}

# --- Земельные участки: цены €/сотка ---
LAND_PRICES = {
    "Centru": 8000,
    "Botanica": 4000,
    "Buiucani": 3500,
    "Râșcani": 3000,
    "Telecentru": 2800,
    "Ciocana": 2500,
    "Posta Veche": 2000,
    "Durlești": 2200,
    "Aeroport": 1500,
    "Sculeni": 2700
}

# --- Коммерческая недвижимость €/м² по районам ---
COMMERCIAL_DISTRICT_PRICES = {
    "Centru": 1300,
    "Botanica": 1000,
    "Buiucani": 1100,
    "Râșcani": 1100,
    "Ciocana": 950,
    "Telecentru": 1000,
    "Posta Veche": 900,
    "Durlești": 850,
    "Aeroport": 800,
    "Sculeni": 950
}

# --- Коэффициенты для разных типов коммерческих объектов ---
COMMERCIAL_COEFFICIENTS = {
    "office": 1.0,
    "store": 1.2,
    "restaurant": 1.3,
    "warehouse": 0.7,
    "production": 0.8
}


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        category = request.form.get("category")

        # КВАРТИРА
        if category == "apartment":
            area = float(request.form.get("area") or 0)
            rooms = int(request.form.get("rooms") or 1)
            district = request.form.get("district")
            repair = request.form.get("repair")
            building = request.form.get("building")

            base_price = DISTRICT_PRICES.get(district, 900)
            repair_coeff = REPAIR_COEFFICIENTS.get(repair, 1.0)
            building_coeff = BUILDING_COEFFICIENTS.get(building, 1.0)
            rooms_coeff = 1.0 + (rooms - 1) * 0.02

            price_per_m2 = base_price * repair_coeff * building_coeff * rooms_coeff
            total_price = area * price_per_m2

            result = {
                "category": "apartment",
                "district": district,
                "rooms": rooms,
                "area": area,
                "repair": repair,
                "building": building,
                "price_per_m2": round(price_per_m2),
                "total_price": round(total_price),
            }

        # ЗЕМЛЯ
        elif category == "land":
            land_area = float(request.form.get("land_area") or 0)
            land_district = request.form.get("land_district")
            price_per_sotka = LAND_PRICES.get(land_district, 2000)
            total_price = land_area * price_per_sotka

            result = {
                "category": "land",
                "district": land_district,
                "land_area": land_area,
                "price_per_sotka": price_per_sotka,
                "total_price": round(total_price)
            }

        # КОММЕРЦИЯ
        elif category == "commercial":
            obj_area = float(request.form.get("object_area") or 0)
            object_type = request.form.get("object_type")
            district = request.form.get("district_com")

            base_price = COMMERCIAL_DISTRICT_PRICES.get(district, 1000)
            type_coeff = COMMERCIAL_COEFFICIENTS.get(object_type, 1.0)
            price_per_m2 = base_price * type_coeff
            total_price = obj_area * price_per_m2

            result = {
                "category": "commercial",
                "district": district,
                "object_area": obj_area,
                "object_type": object_type,
                "price_per_m2": round(price_per_m2),
                "total_price": round(total_price)
            }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
