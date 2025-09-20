from flask import Flask, render_template, request
import math

app = Flask(__name__)

# базовые цены по районам (€/м², условно - их можно подтянуть из статистики позже)
district_prices = {
    "Centru": 1100,
    "Telecentru": 950,
    "Ciocana": 800,
    "Buiucani": 900,
    "Posta Veche": 750,
    "Durlești": 700,
    "Botanica": 850,
    "Sculeni": 800,
    "Râșcani": 870,
    "Aeroport": 650
}

# коэффициенты ремонта
repair_coeffs = {
    "Variantă sură": 0.85,
    "Variantă albă": 0.95,
    "Reparație cosmetică": 1.05,
    "Euroreparație": 1.15
}

# коэффициенты по типу зданий
building_coeffs = {
    "Beton": 1.00,
    "Beton celular": 0.95,
    "Bloc": 0.90,
    "Combinat": 0.92,
    "Cotileț": 0.93,
    "Cărămidă": 1.08,
    "Lemn": 0.85,
    "Monolit": 1.12,
    "Panou": 0.88
}


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        category = request.form.get("category")

        if category == "apartment":
            district = request.form.get("district")
            area = float(request.form.get("area"))
            rooms = int(request.form.get("rooms"))
            floor = int(request.form.get("floor"))
            floors_total = int(request.form.get("floors_total"))
            repair = request.form.get("repair")
            building = request.form.get("building")

            # базовая цена
            base_price = district_prices.get(district, 800)

            # корректировки
            price = base_price
            price *= repair_coeffs.get(repair, 1)
            price *= building_coeffs.get(building, 1)

            # этажность
            if floor == 1:
                price *= 0.95
            elif floor == floors_total:
                price *= 0.97

            total_price = price * area

            result = {
                "category": "Квартира",
                "district": district,
                "area": area,
                "rooms": rooms,
                "floor": floor,
                "floors_total": floors_total,
                "repair": repair,
                "building": building,
                "price_per_m2": round(price, 2),
                "total_price": round(total_price, 2)
            }

        elif category == "land":
            land_type = request.form.get("land_type")
            area = float(request.form.get("land_area"))
            base_price = 20000 if land_type == "intracity" else 5000
            total_price = base_price * area
            result = {
                "category": "Земельный участок",
                "land_type": land_type,
                "area": area,
                "total_price": round(total_price, 2)
            }

        elif category == "commercial":
            obj_type = request.form.get("object_type")
            area = float(request.form.get("object_area"))
            base_price = 900 if obj_type == "office" else 700
            total_price = base_price * area
            result = {
                "category": "Нежилая недвижимость",
                "object": obj_type,
                "area": area,
                "total_price": round(total_price, 2)
            }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)