from flask import Flask, request, render_template, redirect, url_for, session
from functools import wraps
from twilio.twiml.messaging_response import MessagingResponse
import database
from bot_logic import procesar_mensaje

app = Flask(__name__)
app.secret_key = "cambia_esto_por_algo_secreto_unico"  # ← ¡Cambia esto!

database.crear_tablas()
database.crear_admin_inicial()


# ── Decorador para proteger rutas ──────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


# ── Login ──────────────────────────────────────────────────────────────────────
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        usuario = request.form.get("usuario", "")
        contrasena = request.form.get("contrasena", "")
        if database.verificar_admin(usuario, contrasena):
            session["admin"] = usuario
            return redirect(url_for("dashboard"))
        error = "Usuario o contraseña incorrectos"
    return render_template("login.html", error=error)


# ── Logout ─────────────────────────────────────────────────────────────────────
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))


# ── Webhook WhatsApp ───────────────────────────────────────────────────────────
@app.route("/webhook", methods=["POST"])
def webhook():
    mensaje = request.form.get("Body", "")
    numero = request.form.get("From", "")
    database.guardar_usuario(numero)
    database.guardar_mensaje(numero, mensaje)
    respuesta_texto = procesar_mensaje(numero, mensaje)
    resp = MessagingResponse()
    resp.message(respuesta_texto)
    return str(resp)


# ── Dashboard (protegido) ──────────────────────────────────────────────────────
@app.route("/dashboard")
@login_required
def dashboard():
    usuarios = database.obtener_usuarios()
    mensajes = database.obtener_mensajes()
    return render_template(
        "dashboard.html",
        usuarios=usuarios,
        mensajes=mensajes,
        total_usuarios=len(usuarios),
        total_mensajes=len(mensajes),
        admin=session["admin"]
    )


@app.route("/")
def home():
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)