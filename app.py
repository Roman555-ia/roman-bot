from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = "EAAbxWhQZCN0cBRr8SdNEGqbiNsqvPkBrZC52aSz7ZBDNILvYjZAvJ0CZCDOZA71YgIHnphc2ssfgHso5o1NDagPYtGwghsSUGI2hpg3iY5HNxuMmTxxnZAs8WDZC4WYxgCUYiPhtifwE22o8F8ahkak6r0U0TFmiBgfxt2ktZAu8ZASCYG0l7TAh6wonhLomGH2PYvIPc3YLzLZACVetE8HFvQGyr2MnvcxaQb0LA94F0m7mbZCFIERATM0hwYmWynvs25xPr8DPGtWfsGHsSd40O1HOPTPe0wZDZD"
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

    if "hola" in mensaje or "buenas" in mensaje or "info" in mensaje or "información" in mensaje:
        return (
            "👋 Hola, somos *Velnorix*.\n\n"
            "Creamos chatbots para WhatsApp que ayudan a negocios a responder automáticamente a sus clientes.\n\n"
            "Puedes escribir:\n"
            "💰 precios\n"
            "🤖 servicios\n"
            "📅 agendar\n"
            "🕘 horario\n"
            "📍 ubicación\n"
            "❓ cómo funciona"
        )

    elif "precio" in mensaje or "precios" in mensaje or "costo" in mensaje or "cuanto" in mensaje or "cuánto" in mensaje:
        return (
            "💰 *Precios de Velnorix:*\n\n"
            "✅ Instalación del chatbot: *$50*\n"
            "✅ Mensualidad: *$30*\n\n"
            "La instalación incluye configuración inicial, respuestas básicas del negocio y conexión del bot."
        )

    elif "servicio" in mensaje or "servicios" in mensaje or "bot" in mensaje or "chatbot" in mensaje:
        return (
            "🤖 *Servicios de Velnorix:*\n\n"
            "✅ Chatbot para WhatsApp\n"
            "✅ Respuestas automáticas 24/7\n"
            "✅ Información de precios, horarios y servicios\n"
            "✅ Agendamiento de citas\n"
            "✅ Atención inicial para clientes\n"
            "✅ Personalización según tu negocio\n\n"
            "Ideal para barberías, tiendas, restaurantes, spas, gimnasios y emprendimientos."
        )

    elif "horario" in mensaje or "atienden" in mensaje or "hora" in mensaje:
        return (
            "🕘 *Horario de atención Velnorix:*\n\n"
            "Atendemos todos los días de *16:00 a 00:00*.\n\n"
            "También puedes dejarnos tu mensaje y te responderemos apenas estemos disponibles."
        )

    elif "ubicacion" in mensaje or "ubicación" in mensaje or "direccion" in mensaje or "dirección" in mensaje:
        return (
            "📍 *Velnorix no tiene local físico.*\n\n"
            "Trabajamos de manera directa con el cliente, por WhatsApp, videollamada o visita a domicilio según el caso."
        )

    elif "agendar" in mensaje or "cita" in mensaje or "reunion" in mensaje or "reunión" in mensaje or "reservar" in mensaje:
        return (
            "📅 Perfecto, podemos agendar una cita.\n\n"
            "Por favor envíanos estos datos:\n\n"
            "👤 Nombre:\n"
            "🏪 Tipo de negocio:\n"
            "📲 Número de WhatsApp del negocio:\n"
            "📆 Día disponible:\n"
            "🕘 Hora disponible:\n\n"
            "Un asesor de Velnorix revisará tu solicitud y te confirmará la cita."
        )

    elif "como funciona" in mensaje or "cómo funciona" in mensaje or "funciona" in mensaje:
        return (
            "⚙️ *¿Cómo funciona el chatbot de Velnorix?*\n\n"
            "1️⃣ El cliente escribe a tu WhatsApp.\n"
            "2️⃣ El bot responde automáticamente.\n"
            "3️⃣ Puede dar precios, horarios, servicios y agendar citas.\n"
            "4️⃣ Si el cliente necesita atención humana, tú puedes continuar la conversación.\n\n"
            "Así tu negocio no pierde clientes aunque estés ocupado."
        )

    elif "demo" in mensaje or "prueba" in mensaje:
        return (
            "🚀 Sí, podemos mostrarte una demo del chatbot.\n\n"
            "Escríbenos:\n"
            "👤 Tu nombre\n"
            "🏪 Tu tipo de negocio\n"
            "📆 Día y hora para la demostración\n\n"
            "Y coordinamos contigo."
        )

    elif "gracias" in mensaje or "ok" in mensaje or "listo" in mensaje:
        return (
            "Con gusto 🙌\n\n"
            "Velnorix está para ayudarte a automatizar la atención de tu negocio."
        )

    else:
        return (
            "👋 Hola, soy el asistente virtual de *Velnorix* 🤖\n\n"
            "Puedo ayudarte con:\n\n"
            "💰 precios\n"
            "🤖 servicios\n"
            "📅 agendar una cita\n"
            "🕘 horario\n"
            "📍 ubicación\n"
            "⚙️ cómo funciona\n\n"
            "Escribe una de esas opciones para continuar."
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
