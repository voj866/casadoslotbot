import os
import random
import time
import logging
from telegram import Bot, InputFile
from apscheduler.schedulers.blocking import BlockingScheduler

# ====== 設定 ======
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = "@casadoslotbet"
IMAGE_DIR = "images"
DEFAULT_CAPTIONS = [
    "🎁 Nao perca nossas promocoes incriveis hoje! Aproveite os bonus e ganhe mais!",
    "💥 Novos premios esperam por voce! Entre agora e participe das ofertas!",
    "🎰 Varios jogos de slot disponiveis com premios gigantes. Clique e jogue!",
    "🔥 Oportunidades unicas hoje no CASA DO SLOT. Venha conferir!",
    "🤑 Ganhe bonus em cada rodada. Jogue agora no nosso canal oficial!"
]

import os
from telegram import Bot

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise Exception("TELEGRAM_BOT_TOKEN not set!")

bot = Bot(token=TOKEN)

scheduler = BlockingScheduler()

def send_image_with_caption():
    try:
        images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not images:
            logging.warning("No images found.")
            return
        image_file = random.choice(images)
        caption = random.choice(DEFAULT_CAPTIONS)

        with open(os.path.join(IMAGE_DIR, image_file), 'rb') as photo:
            bot.send_photo(chat_id=CHANNEL_ID, photo=InputFile(photo), caption=caption)
        logging.info(f"Sent: {image_file}")
    except Exception as e:
        logging.error(f"Error: {e}")

# 每小時發送一次
scheduler.add_job(send_image_with_caption, 'interval', hours=1)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    send_image_with_caption()  # 啟動時先發送一次
    scheduler.start()
