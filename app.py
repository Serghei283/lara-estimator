from flask import Flask, render_template, request

app = Flask(__name__)

# Базовые цены по районам (€/м²) - реальные цены 2024
DISTRICT_PRICES = {
    "Centru": 1400,
    "Telecentru": 1100,
    "Ciocana": 950,
    "Buiucani": 1150,
    "Posta Veche": 1000,
    "Durlești": 980,
    "Botanica": 1200,
    "Sculeni": 1050,
    "Râșcani": 1100,
    "Aeroport": 900
}

# Коэффициенты ремонта
REPAIR_COEFFICIENTS = {
    "Variantă sură": 0.75,
    "Variantă albă": 0.85,
    "Reparație cosmetică": 0.95,
    "Euroreparație": 1.15
}

# Коэффициенты типа здания
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

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    
    if request.method == "POST":
        # Получаем данные формы
        district = request.form.get("district")
        rooms = int(request.form.get("rooms", 1))
        area = float(request.form.get("area", 0))
        repair = request.form.get("repair")
        building = request.form.get("building")
        floor = int(request.form.get("floor", 2))
        total_floors = int(request.form.get("total_floors", 5))
        
        # Базовая цена по району
        base_price = DISTRICT_PRICES.get(district, 1000)
        
        # Применяем коэффициенты
        repair_coeff = REPAIR_COEFFICIENTS.get(repair, 1.0)
        building_coeff = BUILDING_COEFFICIENTS.get(building, 1.0)
        
        # Коэффициент количества комнат
        rooms_coeff = 1.0 + (rooms - 1) * 0.03
        
        # Коэффициент этажа
        floor_coeff = 1.0
        if floor == 1:
            floor_coeff = 0.95  # первый этаж
        elif floor == total_floors:
            floor_coeff = 0.97  # последний этаж
        
        # Итоговая цена за м²
        price_per_m2 = base_price * repair_coeff * building_coeff * rooms_coeff * floor_coeff
        total_price = area * price_per_m2
        
        result = {
            "district": district,
            "rooms": rooms,
            "area": area,
            "repair": repair,
            "building": building,
            "floor": floor,
            "total_floors": total_floors,
            "price_per_m2": round(price_per_m2),
            "total_price": round(total_price),
            "base_price": base_price,
            "repair_coeff": repair_coeff,
            "building_coeff": building_coeff,
            "rooms_coeff": round(rooms_coeff, 2),
            "floor_coeff": floor_coeff
        }
    
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




