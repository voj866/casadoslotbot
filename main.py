import os
import random
import time
import logging
from telegram import Bot, InputFile
from PIL import Image

logging.basicConfig(level=logging.INFO)

# 讀取環境變數
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise Exception("❌ TELEGRAM_BOT_TOKEN not set! 環境變數未傳入 Railway")

logging.info("✅ Token 成功讀取")
bot = Bot(token=TOKEN)

CHANNEL_ID = -1001234567890
FALLBACK_CAPTIONS = [
    "Nao perca nossas promocoes especiais! 🎉",
    "Novos bonus e recompensas estao te esperando! 💸",
    "Ganhe muito com nossas slots hoje! 🍀",
    "Clique e participe das ofertas imperdiveis! 🤑"
]
IMAGE_FOLDER = "images"

def generate_caption_from_image(image_path):
    keywords = ["jackpot", "bonus", "roleta", "cassino", "777", "dinheiro"]
    return f"Ganhe premios incriveis com {random.choice(keywords).upper()} hoje mesmo! 💥"

def send_random_post():
    try:
        images = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not images:
            logging.error("❌ 找不到任何圖片在 /images 資料夾中")
            return
        image_file = random.choice(images)
        image_path = os.path.join(IMAGE_FOLDER, image_file)

        with Image.open(image_path) as img:
            img.verify()

        caption = generate_caption_from_image(image_path)

        with open(image_path, 'rb') as photo:
            bot.send_photo(chat_id=CHANNEL_ID, photo=InputFile(photo), caption=caption)
            logging.info(f"✅ 已發送圖片：{image_file}")

    except Exception as e:
        logging.error(f"❌ 發送圖片失敗：{e}")

if __name__ == "__main__":
    while True:
        send_random_post()
        time.sleep(3600)
