import os
import logging
import random
from telegram import Bot, InputFile
from apscheduler.schedulers.blocking import BlockingScheduler

# 設定 logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 讀取 BOT TOKEN
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise Exception("❌ TELEGRAM_BOT_TOKEN not set! 環境變數未傳入 Railway")

bot = Bot(token=TOKEN)

# ✅ 使用數字 ID（不要用 @username）
CHANNEL_ID = "-1002712880070"

# 圖片資料夾路徑
IMAGE_FOLDER = "images"

# 預設文案
DEFAULT_CAPTION = "🎰 Ganhe premios agora no CASA DO SLOT! 🎁 Cadastre-se e aproveite: https://casadoslot.com.br"

# 可辨識圖名對應文案（範例）
KEYWORDS = {
    "jackpot": "🎉 Voce pode ganhar o JACKPOT hoje! Jogue agora!",
    "bonus": "💰 Bonus especial disponivel por tempo limitado!",
    "spins": "🌀 Rodadas gratis te esperam. Nao perca!",
}

def generate_caption(filename):
    lower_name = filename.lower()
    for keyword, caption in KEYWORDS.items():
        if keyword in lower_name:
            return caption
    return DEFAULT_CAPTION

def send_random_post():
    try:
        files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]
        if not files:
            logger.warning("⚠️ 沒有圖片可發送")
            return
        file = random.choice(files)
        path = os.path.join(IMAGE_FOLDER, file)
        caption = generate_caption(file)

        bot.send_photo(chat_id=CHANNEL_ID, photo=InputFile(path), caption=caption)
        logger.info(f"✅ 已發送圖片: {file}")
    except Exception as e:
        logger.error(f"❌ 發送失敗: {e}")

if __name__ == "__main__":
    logger.info("✅ Token 成功讀取")
    send_random_post()

    # 設定每小時執行一次
    scheduler = BlockingScheduler()
    scheduler.add_job(send_random_post, "interval", hours=1)
    scheduler.start()
