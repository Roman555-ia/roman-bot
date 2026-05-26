
from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "EAAbxWhQZCN0cBRhOeZCikd4QEOsFaNGCFmL2PlSyFPU5kWKNQy6JLux6ICrIBCca6z9CD4czG0ahVb2lEeNAZBeGttTMsjfa2W233VH9MNc4LD6r3EMvikJwvceQi10vhMyiktiVJBlfzjsDsTfi7ZBxWGNrsX3NnibdioEcAaG3MhZAxQKRZCp0ejhDyqNi76FbPFtElQesE4zagP7ZB0vQRKCEeDFb4rbBsgDgwoK0mgzLzxRQaMknhTP7fZCuj1KeVTZBZCEoEg82HJZC45gfRkxwA19"
PHONE_NUMBER_ID = "1048936894977568"
VERIFY_TOKEN = "roman123"


@app.route("/", methods=["GET"])
def home():
    return "Roman Bot funcionando 🚀"


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
    mensaje_cliente = mensaje_cliente.lower()

    if "precio" in mensaje_cliente:
        respuesta_bot = "💰 Nuestros precios empiezan desde $5."

    elif "horario" in mensaje_cliente:
        respuesta_bot = "🕘 Atendemos de lunes a sábado de 9am a 6pm."

    elif "ubicacion" in mensaje_cliente or "ubicación" in mensaje_cliente:
        respuesta_bot = "📍 Estamos ubicados en Quito. ¿Deseas que te enviemos la dirección exacta?"

    elif "reservar" in mensaje_cliente or "cita" in mensaje_cliente:
        respuesta_bot = "📅 Perfecto. Escríbenos tu nombre, día y hora para reservar."

    else:
        respuesta_bot = "Hola 👋 soy Roman Bot 🤖. Puedes escribir: precio, horario, ubicación o reservar."

    return respuesta_bot


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

    requests.post(url, headers=headers, json=data)


import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

