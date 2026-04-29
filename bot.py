import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# 🔑 Récupère le token depuis Render
TOKEN = os.getenv("TELEGRAM_TOKEN")

# 📁 Fichier de notes
NOTES_PATH = "notes.txt"

# 🤖 Réponse IA (désactivée pour Render)
def ask_ai(prompt):
    return "🤖 IA indisponible pour le moment (bientôt améliorée)"

# 🧠 Gestion des messages
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip().lower()

    # ➤ Ajouter une note
    if user_message.startswith("note:"):
        content = user_message.replace("note:", "").strip()

        with open(NOTES_PATH, "a", encoding="utf-8") as f:
            f.write(f"- {content}\n")

        await update.message.reply_text("📝 Note enregistrée")
        return

    # ➤ Voir les notes
    if user_message == "notes":
        try:
            with open(NOTES_PATH, "r", encoding="utf-8") as f:
                notes = f.read()
        except:
            notes = ""

        await update.message.reply_text(notes if notes else "Aucune note.")
        return

    # ➤ Réponse IA simple
    reply = ask_ai(user_message)
    await update.message.reply_text(reply)


# 🚀 Lancement du bot
app = ApplicationBuilder().token("8608735032:AAFM3bL13e3FKp3vy9v7OsMRcgkb1VlR0dU").build()
app.add_handler(MessageHandler(filters.TEXT, handle))

print("✅ Bot lancé")
app.run_polling()