import os
from flask import Flask, request
import requests
app = Flask(__name__)
VERIFY_TOKEN = "nany123"
PAGE_TOKEN = os.environ.get("PAGE_TOKEN", "EAAXgGaa9bdMBSsNI739i5m4Pn1xKdkMT5aFkaiiH64GznEOE3wOmjvaetVghAcZCNEqFWwZAZBu41HbfJFWw86itaqPoFa4gP11sVNuYupNeLfIRSniYm8Bom5lktaX7Xs80YXXpceTvxyTiiRuGAYUryy9HWREcSlY6M8ZAZCpvZCIXpQR56VyQUepgl7GVMIlvq2mwZDZD")

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Forbidden", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for messaging in entry.get("messaging", []):
                sender_id = messaging.get("sender", {}).get("id")
                if messaging.get("message"):
                    text = messaging["message"].get("text","").lower()
                    reply = "¡Hola! Soy el bot de Nany Novedades 💅\n\n¿Con qué te ayudo hoy?\n1️⃣ Maquillaje\n2️⃣ Filtros\n3️⃣ Hablar con Nany"
                    if "maquillaje" in text or "1" in text:
                        reply = "💄 Maquillaje disponible:\nLabiales, bases, sombras\nEscribe qué buscas y te mando precios 😊"
                    elif "filtro" in text or "2" in text:
                        reply = "✨ Filtros disponibles:\nDime cuál necesitas y te ayudo"
                    elif "nany" in text or "3" in text:
                        reply = "🙋‍♀️ Nany te atenderá en un momento"
                    url = f"https://graph.facebook.com/v20.0/me/messages?access_token={PAGE_TOKEN}"
                    requests.post(url, json={"recipient": {"id": sender_id}, "message": {"text": reply}})
    return "OK", 200

@app.route("/")
def home():
    return "Bot Nany funcionando!"
