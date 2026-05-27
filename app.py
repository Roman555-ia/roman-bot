
from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = "PEGA_AQUI_TU_TOKEN_TEMPORAL_NUEVO"
PHONE_NUMBER_ID = "1048936894977568"
VERIFY_TOKEN = "roman123"

NUMERO_DUENO = "593959473496"

citas_pendientes = {}


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
            print("No es mensaje de cliente.")
            return "ok", 200

        mensaje = value["messages"][0]

        if mensaje.get("type") != "text":
            enviar_mensaje(mensaje["from"], "Por ahora solo puedo responder mensajes de texto 😊")
            return "ok", 200

        numero_cliente = mensaje["from"]
        texto_cliente = mensaje["text"]["body"]

        respuesta_bot = responder(texto_cliente, numero_cliente)
        enviar_mensaje(numero_cliente, respuesta_bot)

    except Exception as error:
        print("ERROR GENERAL:", error)

    return "ok", 200


def responder(mensaje_cliente, numero_cliente):
    mensaje = mensaje_cliente.lower().strip()

    if numero_cliente in citas_pendientes:
        paso = citas_pendientes[numero_cliente]["paso"]

        if paso == "nombre":
            citas_pendientes[numero_cliente]["nombre"] = mensaje_cliente
            citas_pendientes[numero_cliente]["paso"] = "negocio"
            return "🏪 Perfecto. ¿Cuál es el nombre de tu negocio?"

        if paso == "negocio":
            citas_pendientes[numero_cliente]["negocio"] = mensaje_cliente
            citas_pendientes[numero_cliente]["paso"] = "telefono"
            return "📲 ¿Cuál es tu número de contacto?"

        if paso == "telefono":
            citas_pendientes[numero_cliente]["telefono"] = mensaje_cliente
            citas_pendientes[numero_cliente]["paso"] = "dia"
            return "📆 ¿Qué día deseas la cita?"

        if paso == "dia":
            citas_pendientes[numero_cliente]["dia"] = mensaje_cliente
            citas_pendientes[numero_cliente]["paso"] = "hora"
            return "🕘 ¿A qué hora deseas la cita?"

        if paso == "hora":
            citas_pendientes[numero_cliente]["hora"] = mensaje_cliente
            datos = citas_pendientes[numero_cliente]

            mensaje_dueno = (
                "📩 *NUEVA SOLICITUD DE CITA - VELNORIX*\n\n"
                f"👤 Nombre: {datos['nombre']}\n"
                f"🏪 Negocio: {datos['negocio']}\n"
                f"📲 Número: {datos['telefono']}\n"
                f"📆 Día: {datos['dia']}\n"
                f"🕘 Hora: {datos['hora']}\n\n"
                "✅ Contacta al cliente para confirmar la cita."
            )

            enviar_mensaje(NUMERO_DUENO, mensaje_dueno)
            del citas_pendientes[numero_cliente]

            return (
                "✅ Gracias. Hemos recibido tu solicitud de cita.\n\n"
                "Un asesor de *Velnorix* revisará tus datos y se comunicará contigo para confirmar la demostración del chatbot 🤖"
            )

    if "agendar" in mensaje or "cita" in mensaje or "demo" in mensaje or "reservar" in mensaje:
        citas_pendientes[numero_cliente] = {"paso": "nombre"}
        return "📅 Perfecto, vamos a agendar tu cita con Velnorix.\n\n¿Cuál es tu nombre?"

    if "precio" in mensaje or "precios" in mensaje or "costo" in mensaje or "cuánto" in mensaje or "cuanto" in mensaje:
        return (
            "💰 *Precios de Velnorix:*\n\n"
            "✅ Instalación del chatbot: *$50*\n"
            "✅ Mensualidad: *$30*\n\n"
            "Incluye configuración inicial, respuestas básicas del negocio y conexión con WhatsApp."
        )

    if "servicio" in mensaje or "servicios" in mensaje or "chatbot" in mensaje or "bot" in mensaje:
        return (
            "🤖 *Servicios de Velnorix:*\n\n"
            "✅ Chatbots para WhatsApp\n"
            "✅ Respuestas automáticas 24/7\n"
            "✅ Agendamiento manual de citas\n"
            "✅ Información de precios, horarios y servicios\n"
            "✅ Automatización para negocios pequeños\n\n"
            "Ideal para barberías, restaurantes, tiendas, spas, gimnasios y emprendimientos."
        )

    if "horario" in mensaje or "atienden" in mensaje or "hora" in mensaje:
        return (
            "🕘 *Horario de atención Velnorix:*\n\n"
            "Atendemos todos los días de *16:00 a 00:00*."
        )

    if "ubicacion" in mensaje or "ubicación" in mensaje or "direccion" in mensaje or "dirección" in mensaje:
        return (
            "📍 *Velnorix no tiene local físico.*\n\n"
            "Trabajamos directamente con el cliente por WhatsApp, videollamada o atención a domicilio según el caso."
        )

    if "como funciona" in mensaje or "cómo funciona" in mensaje or "funciona" in mensaje:
        return (
            "⚙️ *¿Cómo funciona Velnorix?*\n\n"
            "1️⃣ El cliente escribe a tu WhatsApp.\n"
            "2️⃣ El bot responde automáticamente.\n"
            "3️⃣ Puede dar precios, horarios, servicios y agendar citas.\n"
            "4️⃣ Si el cliente necesita atención humana, tú continúas la conversación.\n\n"
            "Así tu negocio no pierde clientes aunque estés ocupado."
        )

    if "gracias" in mensaje or "ok" in mensaje or "listo" in mensaje:
        return "Con gusto 🙌 Velnorix está para ayudarte a automatizar tu negocio."

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
    print("MENSAJE:", texto)
    print("Respuesta Meta:", respuesta.status_code, respuesta.text)

    return respuesta


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))