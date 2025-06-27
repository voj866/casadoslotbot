import os
import random
import time
from telegram import Bot, InputFile
from PIL import Image
import logging

# 讀取環境變數中的 Token
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise Exception("TELEGRAM_BOT_TOKEN not set!")

bot = Bot(token=TOKEN)
CHANNEL_ID = "@casadoslotbet"
FALLBACK_CAPTIONS = [
    "Nao perca nossas promocoes especiais! 🎉",
    "Novos bonus e recompensas estao te esperando! 💸",
    "Ganhe muito com nossas slots hoje! 🍀",
    "Clique e participe das ofertas imperdiveis! 🤑"
]

# 圖片資料夾
IMAGE_FOLDER = "images"

# 模擬 AI 生成文案（可替換成真 AI 調用）
def generate_caption_from_image(image_path):
    # 模擬圖片分析內容關鍵字（這裡隨機）
    keywords = ["jackpot", "bonus", "roleta", "cassino", "777", "dinheiro"]
    k = random.choice(keywords)
    return f"Ganhe premios incriveis com {k.upper()} hoje mesmo! 💥"

# 發送圖片與文案
def send_random_post():
    images = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if not images:
        logging.error("No images found in /images")
        return

    image_file = random.choice(images)
    image_path = os.path.join(IMAGE_FOLDER, image_file)

    try:
        # 確保圖片可以讀
        with Image.open(image_path) as img:
            img.verify()

        caption = generate_caption_from_image(image_path)
    except Exception as e:
        logging.warning(f"AI 分析圖片失敗：{e}，使用預設文案")
        caption = random.choice(FALLBACK_CAPTIONS)

    try:
        with open(image_path, 'rb') as photo:
            bot.send_photo(chat_id=CHANNEL_ID, photo=InputFile(photo), caption=caption)
            print(f"✅ Sent: {image_file}")
    except Exception as e:
        logging.error(f"發送圖片失敗：{e}")

# 每小時執行一次
if __name__ == "__main__":
    while True:
        send_random_post()
        time.sleep(3600)
