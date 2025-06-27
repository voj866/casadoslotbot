import os
import random
import logging
from telegram import Bot, InputFile
from apscheduler.schedulers.blocking import BlockingScheduler

# Logging 設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 環境變數
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise Exception("❌ TELEGRAM_BOT_TOKEN not set! 環境變數未傳入 Railway")

bot = Bot(token=TOKEN)

# 嘗試抓取 chat_id
updates = bot.get_updates()
for update in updates:
    if update.channel_post:
        logger.info(f"📣 頻道 chat_id：{update.channel_post.chat.id}")
    elif update.message:
        logger.info(f"📩 來自聊天 chat_id：{update.message.chat.id}")

# 測試訊息發送（請先確認你的頻道有 username 才能使用這行）
try:
    bot.send_message(chat_id="@casadoslotbet", text="✅ Bot 啟動成功（測試訊息）")
except Exception as e:
    logger.warning(f"⚠️ 發送測試訊息失敗：{e}")

# 頻道 chat_id（等你知道正確數字後要換掉）
CHANNEL_ID = "@casadoslotbet"  # 或者像這樣：-1001234567890

# 發送隨機圖片與說明
def send_random_post():
    try:
        folder = "images"
        files = os.listdir(folder)
        image_files = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]

        if not image_files:
            logger.warning("❌ 找不到圖片")
            return

        selected_image = random.choice(image_files)
        image_path = os.path.join(folder, selected_image)

        # 隨機文字或固定文案
        caption = f"你的圖片：{selected_image}"

        with open(image_path, "rb") as photo:
            bot.send_photo(chat_id=CHANNEL_ID, photo=InputFile(photo), caption=caption)

        logger.info(f"✅ 已發送圖片：{selected_image}")

    except Exception as e:
        logger.error(f"❌ 發送圖片失敗：{e}")

# 測試立即發送一次
send_random_post()

# 設定排程：每小時執行一次
scheduler = BlockingScheduler()
scheduler.add_job(send_random_post, "interval", hours=1)
scheduler.start()
