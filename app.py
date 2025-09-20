from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        category = request.form.get("category")

        # --- Квартиры ---
        if category == "apartment":
            area = float(request.form.get("area", 0))
            district = request.form.get("district", "")

            base_prices = {"Centru": 1200, "Botanica": 1000, "Ciocana": 800}
            base_price = base_prices.get(district, 900)
            total_price = area * base_price

            result = {
                "category": "apartment",
                "district": district,
                "area": area,
                "price_per_m2": base_price,
                "total_price": total_price
            }

        # --- Земля ---
        elif category == "land":
            land_area = float(request.form.get("land_area", 0))
            land_district = request.form.get("land_district", "")

            land_prices = {"Centru": 8000, "Botanica": 4000, "Ciocana": 2500}
            price_per_sotka = land_prices.get(land_district, 2000)
            total_price = land_area * price_per_sotka

            result = {
                "category": "land",
                "district": land_district,
                "land_area": land_area,
                "price_per_sotka": price_per_sotka,
                "total_price": total_price
            }

        # --- Коммерция ---
        elif category == "commercial":
            obj_area = float(request.form.get("object_area", 0))
            object_type = request.form.get("object_type", "")
            district_com = request.form.get("district_com", "")

            base_prices = {"Centru": 1300, "Botanica": 1000, "Ciocana": 900}
            type_coeff = {
                "office": 1.0,
                "store": 1.2,
                "restaurant": 1.3,
                "warehouse": 0.7,
                "production": 0.8
            }

            base_price = base_prices.get(district_com, 1000)
            coeff = type_coeff.get(object_type, 1.0)
            price_per_m2 = base_price * coeff
            total_price = obj_area * price_per_m2

            result = {
                "category": "commercial",
                "district": district_com,
                "object_area": obj_area,
                "object_type": object_type,
                "price_per_m2": price_per_m2,
                "total_price": total_price
            }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



