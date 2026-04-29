import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

# 🔑 Variables d’environnement
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 🚨 Vérification
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN manquant")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY manquant")

# 🤖 OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

def ask_ai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(e)
        return "❌ IA indisponible"

# 💬 Telegram
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply = ask_ai(user_text)
    await update.message.reply_text(reply)

def run_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle))
    print("🤖 Bot lancé")
    app.run_polling()

# 🌐 Flask (pour Render)
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "OK"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)

# 🚀 Lancement CORRECT (fix threading)
def start():
    threading.Thread(target=run_web).start()  # Flask en secondaire
    run_bot()  # Telegram en principal

if __name__ == "__main__":
    start()