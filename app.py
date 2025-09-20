from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        category = request.form.get("category")

        if category == "apartment":
            try:
                area = float(request.form.get("area") or 0)
                floor = int(request.form.get("floor") or 0)
                floors_total = int(request.form.get("floors_total") or 0)
            except:
                area = 0
                floor = 0
                floors_total = 0

            price_per_m2 = 850
            if floor == 1:
                price_per_m2 *= 0.95
            elif floor == floors_total and floors_total > 1:
                price_per_m2 *= 0.97

            total_price = area * price_per_m2

            result = {
                "category": "apartment",
                "total_price": round(total_price),
                "price_per_m2": round(price_per_m2),
                "district": request.form.get("district"),
                "rooms": request.form.get("rooms"),
                "floor": floor,
                "floors_total": floors_total,
                "repair": request.form.get("repair"),
                "building": request.form.get("building"),
                "area": area
            }

        elif category == "land":
            try:
                land_area = float(request.form.get("land_area") or 0)
            except:
                land_area = 0
            
            price_per_sotka = 1000
            total_price = land_area * price_per_sotka

            result = {
                "category": "land",
                "total_price": round(total_price),
                "land_area": land_area,
                "price_per_sotka": price_per_sotka
            }

        elif category == "commercial":
            try:
                obj_area = float(request.form.get("object_area") or 0)
            except:
                obj_area = 0
            
            price_per_m2 = 1200
            total_price = obj_area * price_per_m2

            result = {
                "category": "commercial",
                "total_price": round(total_price),
                "object_area": obj_area,
                "price_per_m2": price_per_m2
            }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

