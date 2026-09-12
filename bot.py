import re
import urllib.parse
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8664429892:AAGl0JrDDtRf8YIoN-8cv_XKslDXot5HKLU"

def convert_link(text):
    pattern = r"https?://\S+"
    
    match = re.search(pattern, text)
    if not match:
        return None
    
    original = match.group(0)
    encoded = urllib.parse.quote(original, safe='')
    
    return f"https://www.facebook.com/l.php?u={encoded}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    new_link = convert_link(text)

    if new_link:
        await update.message.reply_text(new_link, disable_web_page_preview=False)
    else:
        await update.message.reply_text("No link found")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
