from flask import Flask, render_template, request, jsonify
import qrcode
import os
from datetime import datetime

app = Flask(__name__)

# 📂 Carpeta donde se guardarán los QR
QR_FOLDER = "static/qr_codes"
os.makedirs(QR_FOLDER, exist_ok=True)

# 🌍 Variable global para guardar las coordenadas más recientes
coords = {"lat": 19.4326, "lng": -99.1332}  # CDMX por defecto

# 🔹 Página principal
@app.route("/")
def index():
    return render_template("index.html")

# 🔹 Página del generador de QR
@app.route("/generadorQR", methods=["GET", "POST"])
def generadorQR():
    qr_filename = None
    if request.method == "POST":
        # URL personalizada o raíz del servidor
        data = request.form.get("url") or request.url_root.strip("/")

        # Generar QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Guardar con nombre único
        qr_filename = f"{QR_FOLDER}/qr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        img.save(qr_filename)

    return render_template("generadorQR.html", qr_filename=qr_filename)

# 🔹 Página del mapa (muestra coordenadas)
@app.route("/mapa")
def mapa():
    return render_template("mapa.html")

# 🔹 Endpoint para ACTUALIZAR coordenadas (lo usará la app móvil)
@app.route("/update_coords", methods=["POST"])
def update_coords():
    global coords
    data = request.get_json()
    if "lat" in data and "lng" in data:
        coords["lat"] = float(data["lat"])
        coords["lng"] = float(data["lng"])
        print(f"📡 Coordenadas actualizadas: {coords}")
        return jsonify({"status": "ok", "coords": coords})
    return jsonify({"status": "error", "msg": "Datos inválidos"}), 400

# 🔹 Endpoint para obtener las coordenadas (lo consulta la página web)
@app.route("/get_coords")
def get_coords():
    return jsonify(coords)

# 🔹 Página de login/registro unificada
@app.route("/login", methods=["GET", "POST"])
def login():
    message = None
    if request.method == "POST":
        action = request.form.get("action")
        usuario = request.form.get("usuario")
        password = request.form.get("password")
        email = request.form.get("email")  # solo para registro

        if action == "login":
            message = f"Intento de inicio de sesión con usuario: {usuario}"
        elif action == "register":
            message = f"Intento de registro con usuario: {usuario} y email: {email}"

    return render_template("login.html", message=message)

# 🔹 Logout (cerrar sesión)
@app.route("/logout")
def logout():
    return "Sesión cerrada. <a href='/'>Volver al inicio</a>"

if __name__ == "__main__":
    app.run(debug=True)
