import json
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "7790531310:AAFkK83FK_vqleBZnfGel_JWbKbfqXfKK4w"
CHANNEL_ID = "@agnisinghmodel"

def load_media_map():
    try:
        with open("media_map.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading media_map.json: {e}")
        return {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send a keyword to get the media.")

async def handle_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text.strip()
    media_map = load_media_map()

    if prompt in media_map:
        message_id = media_map[prompt]
        try:
            await context.bot.forward_message(
                chat_id=update.effective_chat.id,
                from_chat_id=CHANNEL_ID,
                message_id=message_id
            )
        except Exception as e:
            print(f"Error forwarding message: {e}")
            await update.message.reply_text("Error sending the media.")
    else:
        await update.message.reply_text("No media found for that keyword.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_prompt))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
