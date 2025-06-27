import os
import random
import logging
from telegram import Bot, InputFile
from apscheduler.schedulers.blocking import BlockingScheduler

# Logging 設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 環境變數讀取
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise Exception("❌ TELEGRAM_BOT_TOKEN not set! 環境變數未傳入 Railway")
bot = Bot(token=TOKEN)

# ✅ 正確的頻道 chat_id（務必加上 -100 前綴）
CHANNEL_ID = -1001069516114

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

        caption = f"你的圖片：{selected_image}"

        with open(image_path, "rb") as photo:
            bot.send_photo(chat_id=CHANNEL_ID, photo=InputFile(photo), caption=caption)

        logger.info(f"✅ 已發送圖片：{selected_image}")

    except Exception as e:
        logger.error(f"❌ 發送圖片失敗：{e}")

# 先發一次測試訊息
send_random_post()

# 每小時定時發送一次
scheduler = BlockingScheduler()
scheduler.add_job(send_random_post, "interval", hours=1)
scheduler.start()
