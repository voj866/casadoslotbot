import os
import random
import time
import logging
from telegram import Bot, InputFile
from PIL import Image

# ✅ 啟用 log 訊息
logging.basicConfig(level=logging.INFO)

# ✅ 讀取 Telegram token（Railway 環境中會自動注入）
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise Exception("❌ TELEGRAM_BOT_TOKEN not set! 環境變數未傳入 Railway")

logging.info("✅ Token 成功讀取")
bot = Bot(token=TOKEN)

# ✅ 設定頻道 ID
CHANNEL_ID = "@casadoslotbet"

# ✅ 預設文案（當 AI 無法辨識圖片時）
FALLBACK_CAPTIONS = [
    "Nao perca nossas promocoes especiais! 🎉",
    "Novos bonus e recompensas estao te esperando! 💸",
    "Ganhe muito com nossas slots hoje! 🍀",
    "Clique e participe das ofertas imperdiveis! 🤑"
]

# ✅ 圖片資料夾路徑
IMAGE_FOLDER = "images"

# ✅ 模擬 AI 根據圖片內容產出文案
def generate_caption_from_image(image_path):
    keywords = ["jackpot", "bonus", "roleta", "cassino", "777", "dinheiro"]
    keyword = random.choice(keywords)
    return f"Ganhe premios incriveis com {keyword.upper()} hoje mesmo! 💥"

# ✅ 發送圖片與文案到 Telegram 頻道
def send_random_post():
    try:
        images = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not images:
            logging.error("❌ 找不到任何圖片在 /images 資料夾中")
            return

        image_file = random.choice(images)
        image_path = os.path.join(IMAGE_FOLDER, image_file)

        # 驗證圖片是否為有效檔案
        try:
            with Image.open(image_path) as img:
                img.verify()
            caption = generate_caption_from_image(image_path)
        except Exception as e:
            logging.warning(f"⚠️ AI 分析圖片失敗：{e}，改用預設文案")
            caption = random.choice(FALLBACK_CAPTIONS)

        with open(image_path, 'rb') as photo:
            bot.send_photo(chat_id=CHANNEL_ID, photo=InputFile(photo), caption=caption)
            logging.info(f"✅ 已發送圖片：{image_file}")

    except Exception as e:
        logging.error(f"❌ 發送圖片過程中出錯：{e}")

# ✅ 每小時發送一次
if __name__ == "__main__":
    while True:
        send_random_post()
        time.sleep(3600)
