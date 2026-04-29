import requests
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# 🔒 CONFIG
TOKEN = "TON_TOKEN_ICI"
OLLAMA_URL = "http://localhost:11434/api/generate"
NOTES_PATH = "C:\\AI\\Notes\\journal.md"

logging.basicConfig(level=logging.INFO)

# 🧠 IA
def ask_ollama(prompt):
    try:
        data = {
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(OLLAMA_URL, json=data, timeout=10)
        result = response.json()
        return result.get("response", "⚠️ Réponse vide")
    except Exception as e:
        logging.error(f"Erreur Ollama: {e}")
        return "⚠️ Erreur IA"

# 📝 Lire notes
def read_notes():
    try:
        with open(NOTES_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

# ✍️ Ajouter note
def add_note(content):
    try:
        with open(NOTES_PATH, "a", encoding="utf-8") as f:
            f.write(f"- {content}\n")
        return True
    except:
        return False

# 🤖 BOT
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_message = update.message.text.strip()

        # ➤ Ajouter note
        if user_message.lower().startswith("note:"):
            content = user_message[5:].strip()
            if add_note(content):
                await update.message.reply_text("📝 Note enregistrée")
            else:
                await update.message.reply_text("❌ Erreur sauvegarde")
            return

        # ➤ Lire notes
        if user_message.lower() == "notes":
            notes = read_notes()
            await update.message.reply_text(notes if notes else "Aucune note.")
            return

        # ➤ Charger mémoire
        notes = read_notes()

        # 🧠 PROMPT INTELLIGENT
        prompt = f"""Tu es un assistant personnel.

Voici mes notes personnelles :
{notes}

Instructions :
- Utilise les notes pour répondre
- Si une tâche est mentionnée → propose une action
- Si la réponse est dans les notes → donne-la directement
- Sinon, réponds normalement mais brièvement

Message :
{user_message}
"""

        reply = ask_ollama(prompt)
        await update.message.reply_text(reply)

    except Exception as e:
        logging.error(f"Erreur bot: {e}")
        await update.message.reply_text("⚠️ Erreur interne")

# 🚀 Lancement
app = ApplicationBuilder().token("8608735032:AAFM3bL13e3FKp3vy9v7OsMRcgkb1VlR0dU").build()
app.add_handler(MessageHandler(filters.TEXT, handle))

print("✅ Bot lancé avec mémoire intelligente")
app.run_polling(drop_pending_updates=True)