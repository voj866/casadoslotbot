import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 設定 log
logging.basicConfig(level=logging.INFO)

# 讀取 TOKEN
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise Exception("❌ TELEGRAM_BOT_TOKEN not set! 請先在 Railway 設定環境變數")

# /start 指令觸發
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"✅ 這是你的 chat_id：{chat_id}")
    logging.info(f"✅ 使用者互動 chat_id：{chat_id}")

# 主程式
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    logging.info("🚀 Bot 啟動，請在 Telegram 對話輸入 /start")
    app.run_polling()
