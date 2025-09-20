from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        category = request.form.get("category")

        if category == "apartment":
            area = float(request.form.get("area", 0))
            # тестовый фиксированный расчёт (дальше можно будет подогнать формулы)
            price_per_m2 = 850
            total_price = area * price_per_m2

            result = {
                "category": "Квартира",
                "total_price": round(total_price),
                "price_per_m2": price_per_m2,
                "district": request.form.get("district"),
                "rooms": request.form.get("rooms"),
                "floor": request.form.get("floor"),
                "floors_total": request.form.get("floors_total"),
                "repair": request.form.get("repair"),
                "building": request.form.get("building"),
                "area": area
            }

        elif category == "land":
            land_area = float(request.form.get("land_area", 0))
            price_per_sotka = 1000
            total_price = land_area * price_per_sotka

            result = {
                "category": "Земельный участок",
                "total_price": round(total_price),
                "land_area": land_area
            }

        elif category == "commercial":
            obj_area = float(request.form.get("object_area", 0))
            price_per_m2 = 1200
            total_price = obj_area * price_per_m2

            result = {
                "category": "Нежилая недвижимость",
                "total_price": round(total_price),
                "object_area": obj_area
            }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
