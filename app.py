
from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = "EAAbxWhQZCN0cBRggs3fJiQV6rK1n0fbbSF4yIBxfmh8QPuUbAbgiBJCAhNqHKa5gYEaXbJUq756cpA6K8ac6sgkFtZCW9v5ZCoCCCuyXy4NbkihimFrPsZC99I1qx4giDVNxn7CGKOTJP2lhe4YoySRdKKdSZCh0SJXNvw2wvQDyvaaZBDchqgmQ8vWqxuECYZCiHlvaPNZBj1gcJH8rn92OKZARQYxZBFv1OLRZC6i6kZADEWIt44CGOAThrR5g7ZCYBaJJEI7MfZBpKioXZBy1lrpfFv7QI2L"
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
        return challenge, 200

    return "Token incorrecto", 403


@app.route("/webhook", methods=["POST"])
def recibir_mensaje():
    data = request.get_json()
    print("DATA RECIBIDA:", data)

    try:
        value = data["entry"][0]["changes"][0]["value"]

        if "messages" not in value:
            print("Evento recibido, pero no es mensaje de cliente.")
            return "ok", 200

        mensaje = value["messages"][0]
        numero_cliente = mensaje["from"]

        if mensaje.get("type") != "text":
            enviar_mensaje(numero_cliente, "Por ahora solo puedo responder mensajes de texto 😊")
            return "ok", 200

        texto_cliente = mensaje["text"]["body"]
        respuesta_bot = responder(texto_cliente)

        enviar_mensaje(numero_cliente, respuesta_bot)

    except Exception as error:
        print("ERROR GENERAL:", error)

    return "ok", 200


def responder(mensaje_cliente):
    mensaje = mensaje_cliente.lower().strip()

    if "precio" in mensaje or "precios" in mensaje or "costo" in mensaje or "cuánto" in mensaje or "cuanto" in mensaje:
        return (
            "💰 *Precios de Velnorix:*\n\n"
            "✅ Instalación del chatbot: *$50*\n"
            "✅ Mensualidad: *$30*\n\n"
            "Incluye configuración inicial, respuestas básicas del negocio y conexión con WhatsApp."
        )

    elif "servicio" in mensaje or "servicios" in mensaje or "chatbot" in mensaje or "bot" in mensaje:
        return (
            "🤖 *Servicios de Velnorix:*\n\n"
            "✅ Chatbots para WhatsApp\n"
            "✅ Respuestas automáticas 24/7\n"
            "✅ Información de precios, horarios y servicios\n"
            "✅ Atención inicial para clientes\n"
            "✅ Automatización para negocios pequeños\n\n"
            "Ideal para barberías, restaurantes, tiendas, spas, gimnasios y emprendimientos."
        )

    elif "horario" in mensaje or "atienden" in mensaje or "hora" in mensaje:
        return (
            "🕘 *Horario de atención Velnorix:*\n\n"
            "Atendemos todos los días de *16:00 a 00:00*."
        )

    elif "ubicacion" in mensaje or "ubicación" in mensaje or "direccion" in mensaje or "dirección" in mensaje:
        return (
            "📍 *Velnorix no tiene local físico.*\n\n"
            "Trabajamos directamente con el cliente por WhatsApp, videollamada o atención a domicilio según el caso."
        )

    elif "agendar" in mensaje or "cita" in mensaje or "demo" in mensaje or "reservar" in mensaje:
        return (
            "📅 Perfecto, podemos agendar una demostración.\n\n"
            "Por favor envíanos en un solo mensaje:\n\n"
            "👤 Nombre:\n"
            "🏪 Tipo de negocio:\n"
            "📲 Número de contacto:\n"
            "📆 Día disponible:\n"
            "🕘 Hora disponible:\n\n"
            "Un asesor de *Velnorix* revisará tu solicitud y se comunicará contigo para confirmar."
        )

    elif "como funciona" in mensaje or "cómo funciona" in mensaje or "funciona" in mensaje:
        return (
            "⚙️ *¿Cómo funciona Velnorix?*\n\n"
            "1️⃣ El cliente escribe a tu WhatsApp.\n"
            "2️⃣ El bot responde automáticamente.\n"
            "3️⃣ Puede dar precios, horarios y servicios.\n"
            "4️⃣ Si el cliente necesita atención humana, tú continúas la conversación.\n\n"
            "Así tu negocio no pierde clientes aunque estés ocupado."
        )

    elif "gracias" in mensaje or "ok" in mensaje or "listo" in mensaje:
        return "Con gusto 🙌 Velnorix está para ayudarte a automatizar tu negocio."

    else:
        return menu_principal()


def menu_principal():
    return (
        "👋 Hola, soy el asistente virtual de *Velnorix* 🤖\n\n"
        "Creamos chatbots para WhatsApp que ayudan a negocios a responder automáticamente.\n\n"
        "Escribe una opción:\n\n"
        "💰 precios\n"
        "🤖 servicios\n"
        "📅 agendar\n"
        "🕘 horario\n"
        "📍 ubicación\n"
        "⚙️ cómo funciona"
    )


def enviar_mensaje(numero_destino, texto):
    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": numero_destino,
        "type": "text",
        "text": {
            "body": texto
        }
    }

    respuesta = requests.post(url, headers=headers, json=data)

    print("ENVIANDO A:", numero_destino)
    print("RESPUESTA BOT:", texto)
    print("RESPUESTA META:", respuesta.status_code, respuesta.text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))