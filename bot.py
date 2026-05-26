
from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "EAAbxWhQZCN0cBRW5569pUEDmQwb0ZBXczynAhIYx8kGxPKZCfzbIDOhsA8rwR9p5l82Db5VC3atNWsE7c0RGi6gOWOQ3uHZB6BxGX8C4HyFmVkLcqW2BguGgOHXgaoMvOVq8rKvOGmQ5tD6HUsgkURUtSqZBAZCDNUVugA2HVzDyxvZAkpy5FV2fvk7qJ1TR3qjRKukftz2kFZCjzlXGjfzdBj5MXZBWALZBCvtOvlfwzAsVggAsoQJGmgTZCgrkZBNAZCWYc0aZALikLo44sAIMvJxFWGiSft"

PHONE_NUMBER_ID = "1048936894977568"

@app.route("/webhook", methods=["GET"])
def verificar():
    return "Webhook funcionando 🚀"

@app.route("/webhook", methods=["POST"])
def recibir_mensaje():

    data = request.get_json()

    print(data)

    return "ok", 200

def enviar_mensaje(numero, mensaje):

    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {
            "body": mensaje
        }
    }

    requests.post(url, headers=headers, json=data)

if __name__ == "__main__":
    app.run(port=5000)