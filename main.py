import os
import random
import time
import logging
from telegram import Bot, InputFile
from PIL import Image
from dotenv import load_dotenv

# 設定 logging 輸出格式
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# 載入本地 .env 檔（本地開發時使用，Railway 環境不影響）
load_dotenv()

# 從環境變數中取得 Telegram token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise Exception("❌ TELEGRAM_BOT_TOKEN not set! 環境變數未傳入 Railway")

# 建立 bot 實體
bot = Bot(token=TOKEN)
CHANNEL_ID = "@casadoslotbet"

# 預設備用文案（AI 辨識失敗時使用）
FALLBACK_CAPTIONS = [
    "Nao perca nossas promocoes especiais! 🎉",
    "Novos bonus e recompensas estao te esperando! 💸",
    "Ganhe muito com nossas slots hoje! 🍀",
    "Clique e participe das ofertas imperdiveis! 🤑"
]

# 圖片資料夾路徑
IMAGE_FOLDER = "images"

# 模擬圖片 AI 分析回傳文案
def generate_caption_from_image(image_path):
    keywords = ["jackpot", "bonus", "roleta", "cassino", "777", "dinheiro"]
    keyword = random.choice(keywords)
    return f"Ganhe premios incriveis com {keyword.upper()} hoje mesmo! 💥"

# 發送 Telegram 圖片貼文
def send_random_post():
    try:
        images = [
            f for f in os.listdir(IMAGE_FOLDER)
            if f.lower().endswith(('.png', '.jpg', '.jpeg'))
        ]
        if not images:
            logging.error("❌ 找不到任何圖片在 /images 資料夾中")
            return

        image_file = random.choice(images)
        image_path = os.path.join(IMAGE_FOLDER, image_file)

        # 驗證圖片可讀性
        try:
            with Image.open(image_path) as img:
                img.verify()
            caption = generate_caption_from_image(image_path)
        except Exception as e:
            logging.warning(f"⚠️ 圖片無法分析或損毀：{e}，改用預設文案")
            caption = random.choice(FALLBACK_CAPTIONS)

        with open(image_path, 'rb') as photo:
            bot.send_photo(chat_id=CHANNEL_ID, photo=InputFile(photo), caption=caption)
            logging.info(f"✅ 已發送圖片：{image_file}")

    except Exception as e:
        logging.error(f"❌ 發送過程錯誤：{e}")

# 主流程：每 1 小時執行一次
if __name__ == "__main__":
    logging.info("🚀 Bot 開始執行，每小時自動發送圖片與文案...")
    while True:
        send_random_post()
        time.sleep(3600)
