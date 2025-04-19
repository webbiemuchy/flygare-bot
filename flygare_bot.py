import logging
import pytesseract
import cv2
import numpy as np
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from io import BytesIO

logging.basicConfig(level=logging.INFO)

TOKEN = '7931589149:AAEYQUBGOFIgn8RaGp07K4GgOQ_U_BUU-Uo'

def analyze_multipliers(multipliers):
    nums = [float(x.replace('x', '')) for x in multipliers if 'x' in x]
    if not nums:
        return "Couldn't detect valid multipliers."

    low = [x for x in nums if x < 1.5]
    high = [x for x in nums if x > 10]
    avg = sum(nums) / len(nums)
    median = sorted(nums)[len(nums)//2]

    return f"""*Aviator Analyzer*
Rounds analyzed: {len(nums)}
Average: {avg:.2f}x
Median: {median:.2f}x
Low (<1.5x): {len(low)} rounds
High (>10x): {len(high)} rounds

*Strategy Suggestion*:
- Play Safe: Auto cash at 1.5x
- Moderate: Go in after 2 low rounds, target 2x
- Spicy: Wait for 4 low rounds, aim for 10x
"""

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        return

    photo = update.message.photo[-1]
    file = await photo.get_file()
    bio = BytesIO()
    await file.download_to_memory(out=bio)
    bio.seek(0)

    image = cv2.imdecode(p.frombuffer(bio.read(), np.uint8), cv2.IMREAD_COLOR)
    raw_text = pytesseract.image_to_string(image)
    multipliers = [x.strip() for x in raw_text.replace('\n', ' ').split() if 'x' in x]

    result = analyze_multipliers(multipliers)
    await update.message.reply_text(result, parse_mode='Markdown')

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    await app.run_polling()

if __name__ == '_main_':
    import asyncio
    asyncio.run(main())
