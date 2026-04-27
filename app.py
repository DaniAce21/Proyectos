from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import os

app = Flask(__name__)

# 🔐 API KEY desde variable de entorno
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# 🧠 Fallback sin IA (SIEMPRE funciona)
def clasificacion_basica(mensaje):
    mensaje = mensaje.lower()

    if "comprar" in mensaje or "precio" in mensaje:
        return "ventas"
    elif "problema" in mensaje or "error" in mensaje:
        return "soporte"
    else:
        return "general"


# 🤖 Clasificación con IA + fallback
def clasificar_mensaje(mensaje):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"Clasifica este mensaje en una palabra: ventas, soporte o general.\nMensaje: {mensaje}"
                }
            ],
            max_tokens=10
        )

        categoria = response.choices[0].message.content.strip().lower()

        if categoria not in ["ventas", "soporte", "general"]:
            return clasificacion_basica(mensaje)

        return categoria

    except Exception as e:
        print(f"⚠️ Error con OpenAI: {e}")
        print("👉 Usando fallback sin IA")
        return clasificacion_basica(mensaje)


# 📩 Webhook de WhatsApp
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.form.get("Body")

    print(f"📩 Mensaje recibido: {incoming_msg}")

    if not incoming_msg:
        return "No message received", 400

    categoria = clasificar_mensaje(incoming_msg)

    # 💬 Respuestas
    if categoria == "ventas":
        respuesta = "💰 Gracias por tu interés en ventas. Te contactaremos pronto."
    elif categoria == "soporte":
        respuesta = "🛠️ Recibimos tu solicitud de soporte. Te ayudaremos en breve."
    else:
        respuesta = "📩 Gracias por tu mensaje. Te responderemos pronto."

    resp = MessagingResponse()
    resp.message(respuesta)

    return str(resp)


# ▶️ Ejecutar servidor
if __name__ == "__main__":
    app.run(port=5000, debug=True)