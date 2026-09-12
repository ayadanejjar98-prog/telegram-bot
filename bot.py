from urllib.parse import quote
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, filters
)

BOT_TOKEN = "8907079439:AAHs86KWQdR3b9JKJu96JBUdG3pp--sCJWo"

# Simple anti-spam: one conversion per user every 2 seconds
last_request = {}
stats = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Send me any URL and I'll convert it to a Facebook link.\n\n"
        "Example:\n"
        "https://mirandadeals.com/W3dSmx"
    )

async def convert_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_id = update.effective_user.id
    now = time.time()

    if now - last_request.get(user_id, 0) < 2:
        await update.message.reply_text("⏳ Please wait a moment and try again.")
        return

    last_request[user_id] = now
    text = update.message.text.strip()

    if not text.startswith(("http://", "https://")):
        await update.message.reply_text("❌ Please send a valid URL starting with http:// or https://")
        return

    encoded_url = quote(text, safe="")
    facebook_link = f"https://www.facebook.com/l.php?u={encoded_url}"

    stats[user_id] = stats.get(user_id, 0) + 1

    keyboard = [[
        InlineKeyboardButton("📋 Copy / Open Link", url=facebook_link)
    ]]

    await update.message.reply_text(
        f"✅ Converted!\n\n{facebook_link}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def my_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    count = stats.get(user_id, 0)
    await update.message.reply_text(f"📊 Your conversions: {count}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send any URL and I'll convert it.\n\n"
        "/start - Start the bot\n"
        "/stats - Your conversion count\n"
        "/help - Help"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", my_stats))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, convert_link)
    )

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

