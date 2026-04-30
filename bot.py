import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

# 🔑 Variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN manquant")

# 🤖 OpenAI (optionnel)
client = None
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)

# 🧠 Réponses rapides gratuites
def quick_reply(text):
    text = text.lower()

    if "bonjour" in text or "salut" in text:
        return "👋 Salut !"

    if "ça va" in text:
        return "Oui tranquille 😄"

    if "merci" in text:
        return "Avec plaisir 👍"

    if "heure" in text:
        from datetime import datetime
        return f"🕒 {datetime.now().strftime('%H:%M')}"

    return None

# 🤖 IA (si dispo)
def ask_ai(prompt):
    if not client:
        return None

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except:
        return None

# 💬 Gestion message
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # 1️⃣ réponse rapide
    quick = quick_reply(user_text)
    if quick:
        await update.message.reply_text(quick)
        return

    # 2️⃣ IA
    ai = ask_ai(user_text)
    if ai:
        await update.message.reply_text(ai)
        return

    # 3️⃣ fallback propre
    await update.message.reply_text(
        "🤖 Je réfléchis encore à ça... repose-moi la question autrement 😉"
    )

# 🚀 Telegram
def run_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle))
    print("🤖 Bot lancé")
    app.run_polling()

# 🌐 Flask (Render)
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "OK"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)

# 🔥 lancement correct
def start():
    threading.Thread(target=run_web).start()
    run_bot()

if __name__ == "__main__":
    start()