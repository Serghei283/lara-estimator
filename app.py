from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    
    if request.method == "POST":
        category = request.form.get("category")
        
        if category == "apartment":
            area = float(request.form.get("area", 0))
            district = request.form.get("district", "")
            rooms = int(request.form.get("rooms", 1))
            repair = request.form.get("repair", "")
            building = request.form.get("building", "")
            
            # Базовые цены по районам
            district_prices = {
                "Centru": 1200, "Telecentru": 950, "Ciocana": 800,
                "Buiucani": 950, "Posta Veche": 850, "Durlești": 820,
                "Botanica": 1000, "Sculeni": 900, "Râșcani": 950, "Aeroport": 750
            }
            
            # Коэффициенты ремонта
            repair_coeff = {
                "Variantă sură": 0.75, "Variantă albă": 0.85,
                "Reparație cosmetică": 0.95, "Euroreparație": 1.15
            }
            
            # Коэффициенты здания
            building_coeff = {
                "Beton": 0.95, "Beton celular": 0.90, "Bloc": 0.85,
                "Combinat": 0.88, "Cotileț": 0.92, "Cărămidă": 1.05,
                "Lemn": 0.80, "Monolit": 1.10, "Panou": 0.82
            }
            
            base_price = district_prices.get(district, 900)
            repair_k = repair_coeff.get(repair, 1.0)
            building_k = building_coeff.get(building, 1.0)
            rooms_k = 1.0 + (rooms - 1) * 0.02
            
            price_per_m2 = base_price * repair_k * building_k * rooms_k
            total_price = area * price_per_m2
            
            result = {
                "category": "apartment",
                "total_price": int(total_price),
                "price_per_m2": int(price_per_m2),
                "district": district,
                "area": area,
                "rooms": rooms,
                "repair": repair,
                "building": building
            }
            
        elif category == "land":
            land_area = float(request.form.get("land_area", 0))
            land_district = request.form.get("land_district", "")
            
            land_prices = {
                "Centru": 8000, "Botanica": 4000, "Buiucani": 3500,
                "Râșcani": 3000, "Telecentru": 2800, "Ciocana": 2500,
                "Posta Veche": 2000, "Durlești": 2200, "Aeroport": 1500, "Sculeni": 2700
            }
            
            price_per_sotka = land_prices.get(land_district, 2000)
            total_price = land_area * price_per_sotka
            
            result = {
                "category": "land",
                "total_price": int(total_price),
                "price_per_sotka": price_per_sotka,
                "district": land_district,
                "land_area": land_area
            }
            
        elif category == "commercial":
            obj_area = float(request.form.get("object_area", 0))
            district_com = request.form.get("district_com", "")
            object_type = request.form.get("object_type", "")
            
            commercial_prices = {
                "Centru": 1300, "Botanica": 1000, "Buiucani": 1100,
                "Râșcani": 1100, "Ciocana": 950, "Telecentru": 1000,
                "Posta Veche": 900, "Durlești": 850, "Aeroport": 800, "Sculeni": 950
            }
            
            type_coeff = {
                "office": 1.0, "store": 1.2, "restaurant": 1.3,
                "warehouse": 0.7, "production": 0.8
            }
            
            base_price = commercial_prices.get(district_com, 1000)
            type_k = type_coeff.get(object_type, 1.0)
            price_per_m2 = base_price * type_k
            total_price = obj_area * price_per_m2
            
            result = {
                "category": "commercial",
                "total_price": int(total_price),
                "price_per_m2": int(price_per_m2),
                "district": district_com,
                "object_area": obj_area,
                "object_type": object_type
            }
    
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


