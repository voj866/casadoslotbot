import os
import random
import logging
import time
import asyncio
from datetime import datetime
from telegram import Bot, InputFile
from telegram.ext import Application, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TOKEN")
CHANNEL_ID = "@casadoslotbet"
POST_INTERVAL = 3600  # 每 1 小時一次

# 預設文案清單（AI 無法辨識圖片內容時使用）
fallback_messages = [
    "🎉 Muitas promoções incríveis estão te esperando no Casa do Slot! Aproveite agora!",
    "💰 Bônus imperdíveis só hoje! Não perca!",
    "🎰 Vem jogar com a gente e ganhe prêmios incríveis!",
    "🔥 Promoções ativas 24h por dia, participe!",
]

# 模擬圖片 AI 分析
def ai_generate_caption(filename):
    name = filename.lower()
    if "cashback" in name:
        return "💸 Receba cashback em todas as suas apostas nos slots! Jogue agora!"
    elif "bonus" in name:
        return "🎁 Ganhe bônus especiais em seus depósitos! Até R$5.777!"
    elif "deposito" in name:
        return "💳 Faça seu segundo depósito e concorra a prêmios incríveis!"
    else:
        return random.choice(fallback_messages)

async def post_image(bot: Bot):
    files = os.listdir("images")
    image_file = random.choice(files)
    image_path = f"images/{image_file}"
    caption = ai_generate_caption(image_file)

    with open(image_path, "rb") as img:
        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=InputFile(img),
            caption=caption + "\n\n👉 [Jogue agora](https://www.casadoslot.bet/m/home?affiliateCode=adselontg)",
            parse_mode="Markdown"
        )
    print(f"[{datetime.now()}] 已發送圖片與文案：{image_file}")

async def loop_post(app: Application):
    while True:
        await post_image(app.bot)
        await asyncio.sleep(POST_INTERVAL)

async def main():
    application = Application.builder().token(BOT_TOKEN).build()
    asyncio.create_task(loop_post(application))
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.idle()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
