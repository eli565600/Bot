
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

load_dotenv()

TOKEN = '8227539013:AAECLUP57jNAa_l9GSZGuBg5zNGk0RWrKVo'
ADMIN_ID = 5722257275

if not TOKEN:
    raise RuntimeError("Missing BOT_TOKEN. Put it in .env")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("היי! אני בוט 👋\nשלח /help לראות .")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "פקודות:\n"
        "/start - התחלה\n"
        "/help - עזרה\n"
        "/ping - בדיקה\n"
    )
async def claim_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ADMIN_ID
    ADMIN_ID = update.effective_user.id
    await update.message.reply_text(f"✅ הוגדרת כאדמין. ADMIN_ID = {ADMIN_ID}")


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("pong ✅")
ADMIN_ID = 123456789  # תכניס כאן את ה-User ID שלך

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ADMIN_ID
    if ADMIN_ID is None:
        await update.message.reply_text("האדמין לא הוגדר עדיין. שלח /claim כדי להגדיר.")
        return

    user = update.message.from_user
    text = update.message.text

    message = (
        "📩 הודעה חדשה לבוט\n\n"
        f"👤 From: {user.first_name} (@{user.username})\n"
        f"🆔 ID: {user.id}\n\n"
        f"💬 Message:\n{text}"
    )
    print("📩 הודעה חדשה לבוט\n\n"
        f"👤 From: {user.first_name} (@{user.username})\n"
        f"🆔 ID: {user.id}\n\n"
        f"💬 Message:\n{text}")
    await context.bot.send_message(chat_id=ADMIN_ID, text=message)
    await update.message.reply_text("✅ נשלח לאדמין")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # מחזיר כל טקסט שהמשתמש שולח
    text = update.message.text
    await update.message.reply_text(f"כתבת: {text}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("claim", claim_admin))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin))

    app.run_polling()

if __name__ == "__main__":
    main()
