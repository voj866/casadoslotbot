import os
import random
import logging
from telegram import Bot, InputFile
from apscheduler.schedulers.blocking import BlockingScheduler

# 設定 logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 從環境變數取得 Bot Token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise Exception("❌ TELEGRAM_BOT_TOKEN not set! 環境變數未傳入 Railway")

# ✅ 這裡改成你頻道的 username（公開頻道才有效）
CHANNEL_ID = "@casadoslotbet"

bot = Bot(token=TOKEN)

def send_random_post():
    image_dir = "images"
    images = [f for f in os.listdir(image_dir) if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]

    if not images:
        logger.warning("❌ 沒有找到任何圖片！")
        return

    selected_image = random.choice(images)
    image_path = os.path.join(image_dir, selected_image)
    caption = f"你的圖片：{selected_image}"

    with open(image_path, "rb") as photo:
        bot.send_photo(chat_id=CHANNEL_ID, photo=InputFile(photo), caption=caption)
        logger.info(f"✅ 已發送圖片：{selected_image}")

# 啟動定時任務，每小時執行一次
scheduler = BlockingScheduler()
scheduler.add_job(send_random_post, "interval", hours=1)
send_random_post()  # 啟動時立即發送一次
scheduler.start()
