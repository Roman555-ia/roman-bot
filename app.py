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

        respuesta_bot = responder(mensaje_cliente)
        enviar_mensaje(numero_cliente, respuesta_bot)

    except Exception as error:
        print("Error:", error)

    return "ok", 200


def responder(mensaje_cliente):
    mensaje = mensaje_cliente.lower()

    if "agendar" in mensaje or "cita" in mensaje or "demo" in mensaje or "reservar" in mensaje:
        return (
            "📅 Perfecto, podemos agendar una cita con Velnorix.\n\n"
            "Por favor copia y llena estos datos:\n\n"
            "👤 Nombre:\n"
            "🏪 Tipo de negocio:\n"
            "📲 Número de contacto:\n"
            "📆 Día disponible:\n"
            "🕘 Hora disponible:\n"
            "💬 ¿Qué necesitas automatizar?:\n\n"
            "Cuando nos envíes esos datos, un asesor de Velnorix revisará tu solicitud y te confirmará la cita."
        )

    elif "nombre:" in mensaje and "negocio:" in mensaje:
        return (
            "✅ Gracias. Hemos recibido tu solicitud de cita.\n\n"
            "Un asesor de *Velnorix* revisará tus datos y se comunicará contigo para confirmar la demostración del chatbot 🤖"
        )

    elif "precio" in mensaje or "precios" in mensaje or "costo" in mensaje:
        return (
            "💰 *Precios de Velnorix:*\n\n"
            "✅ Instalación: *$50*\n"
            "✅ Mensualidad: *$30*\n\n"
            "Incluye configuración inicial del chatbot, respuestas básicas y conexión con WhatsApp."
        )

    elif "horario" in mensaje:
        return (
            "🕘 *Horario de atención:*\n\n"
            "Atendemos de *16:00 a 00:00*."
        )

    elif "ubicacion" in mensaje or "ubicación" in mensaje or "direccion" in mensaje:
        return (
            "📍 No tenemos local físico.\n\n"
            "Trabajamos de forma directa con el cliente por WhatsApp, videollamada o atención a domicilio según el caso."
        )

    elif "servicio" in mensaje or "servicios" in mensaje or "chatbot" in mensaje:
        return (
            "🤖 *Servicios de Velnorix:*\n\n"
            "✅ Chatbots para WhatsApp\n"
            "✅ Respuestas automáticas 24/7\n"
            "✅ Agendamiento manual de citas\n"
            "✅ Información de precios, horarios y servicios\n"
            "✅ Automatización para negocios pequeños\n\n"
            "Ideal para barberías, tiendas, restaurantes, spas, gimnasios y emprendimientos."
        )

    elif "hola" in mensaje or "buenas" in mensaje:
        return (
            "👋 Hola, somos *Velnorix*.\n\n"
            "Creamos chatbots para WhatsApp que ayudan a los negocios a responder automáticamente.\n\n"
            "Escribe una opción:\n\n"
            "💰 precios\n"
            "🤖 servicios\n"
            "📅 agendar\n"
            "🕘 horario\n"
            "📍 ubicación"
        )

    else:
        return (
            "👋 Soy el asistente virtual de *Velnorix* 🤖\n\n"
            "Puedo ayudarte con:\n\n"
            "💰 precios\n"
            "🤖 servicios\n"
            "📅 agendar una cita\n"
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
