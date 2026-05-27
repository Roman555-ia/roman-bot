from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = "EAAbxWhQZCN0cBRoZBhlZCJxhZBnY9l5EP5M0CupEUTopxwFGtLcI65FQZAvdZAINDtVQkv7lfNfGaAinYL7qODToanHMcO3z9PYFSQbaPbNrrLsZAMnEPLhZB1SMv5naNzrLWNwZBLiT3Fj6pGfXPE0jXDfZBfpUdzRqq3fKkkhZAGrPVCvCCedeeQIRgZC0uxaiz56BOZARnI5TAOi504UOo2ZAZAZC1alqUJmOTjzFX8ecFDkmaTDZAyhOgXK9aeLw3A9fLZCG3JKxzteO5OTmUs4CFNccLqi9Ws"
PHONE_NUMBER_ID = "1048936894977568"
VERIFY_TOKEN = "roman123"


@app.route("/", methods=["GET"])
def home():
    return "Velnorix Bot funcionando 🚀"


@app.route("/webhook", methods=["GET"])
def verificar():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if token == VERIFY_TOKEN:
        return challenge

    return "Token incorrecto", 403


@app.route("/webhook", methods=["POST"])
def recibir_mensaje():
    data = request.get_json()
    print(data)

    try:
        mensaje_cliente = data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
        numero_cliente = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]

        respuesta_bot = responder(mensaje_cliente, numero_cliente)
        enviar_mensaje(numero_cliente, respuesta_bot)

    except Exception as error:
        print("Error:", error)

    return "ok", 200

def responder(mensaje_cliente, numero_cliente):
    mensaje = mensaje_cliente.lower()

    if numero_cliente in citas_pendientes:
        paso = citas_pendientes[numero_cliente]["paso"]

        if paso == "nombre":
            citas_pendientes[numero_cliente]["nombre"] = mensaje_cliente
            citas_pendientes[numero_cliente]["paso"] = "negocio"
            return "🏪 Perfecto. ¿Cuál es el nombre de tu negocio?"

        elif paso == "negocio":
            citas_pendientes[numero_cliente]["negocio"] = mensaje_cliente
            citas_pendientes[numero_cliente]["paso"] = "numero"
            return "📲 ¿Cuál es tu número de contacto?"

        elif paso == "numero":
            citas_pendientes[numero_cliente]["telefono"] = mensaje_cliente
            citas_pendientes[numero_cliente]["paso"] = "dia"
            return "📆 ¿Qué día deseas la cita?"

        elif paso == "dia":
            citas_pendientes[numero_cliente]["dia"] = mensaje_cliente
            citas_pendientes[numero_cliente]["paso"] = "hora"
            return "🕘 ¿A qué hora deseas la cita?"

        elif paso == "hora":
            citas_pendientes[numero_cliente]["hora"] = mensaje_cliente

            datos = citas_pendientes[numero_cliente]

            mensaje_dueno = (
                "📩 *NUEVA CITA VELNORIX*\n\n"
                f"👤 Nombre: {datos['nombre']}\n"
                f"🏪 Negocio: {datos['negocio']}\n"
                f"📲 Número: {datos['telefono']}\n"
                f"📆 Día: {datos['dia']}\n"
                f"🕘 Hora: {datos['hora']}"
            )

            enviar_mensaje(NUMERO_DUENO, mensaje_dueno)

            del citas_pendientes[numero_cliente]

            return (
                "✅ Gracias. Hemos recibido tu solicitud de cita.\n\n"
                "Un asesor de *Velnorix* se comunicará contigo para confirmar la demostración del chatbot 🤖"
            )

    if "agendar" in mensaje or "cita" in mensaje or "demo" in mensaje:
        citas_pendientes[numero_cliente] = {"paso": "nombre"}
        return "📅 Perfecto, vamos a agendar tu cita. ¿Cuál es tu nombre?"

    return (
        "👋 Hola, soy el asistente virtual de *Velnorix* 🤖\n\n"
        "Puedes escribir:\n"
        "💰 precios\n"
        "🤖 servicios\n"
        "📅 agendar\n"
        "🕘 horario\n"
        "📍 ubicación"
    )
    

def enviar_mensaje(numero_cliente, respuesta_bot):
    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": numero_cliente,
        "type": "text",
        "text": {
            "body": respuesta_bot
        }
    }

    respuesta = requests.post(url, headers=headers, json=data)
    print("Respuesta Meta:", respuesta.status_code, respuesta.text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
