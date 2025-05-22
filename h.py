from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import time

TOKEN = "8088275204:AAGZF85Sk7VA47wfxk7P3SN2hd81cLgS7FQ"
API_URL = "https://api.bdg88zf.com/api/webapi/GetNoaverageEmerdList"

prediction_pattern = [
    "BIG","BIG","SMALL","SMALL","BIG","SMALL","BIG","BIG","SMALL","BIG","SMALL","BIG","SMALL","BIG","SMALL",
    "SMALL","BIG","SMALL","BIG","BIG","SMALL","SMALL","BIG","BIG","SMALL","BIG","SMALL","SMALL","BIG","BIG",
    "BIG","BIG","BIG","SMALL","SMALL","SMALL","BIG","SMALL","BIG","SMALL","BIG","BIG","SMALL","SMALL","BIG",
    "SMALL","BIG","BIG","SMALL","SMALL","BIG","BIG","SMALL","BIG","SMALL","BIG","SMALL","BIG","SMALL","BIG",
    "BIG","SMALL","BIG","SMALL","BIG","BIG","SMALL","BIG","SMALL","BIG","SMALL","BIG","SMALL","SMALL","BIG",
    "SMALL","SMALL","BIG","BIG","BIG","SMALL","BIG","SMALL","SMALL","BIG","SMALL","BIG","BIG","SMALL","BIG",
    "BIG","BIG","SMALL","BIG","SMALL","SMALL","BIG","SMALL","BIG","SMALL","BIG","SMALL","BIG","SMALL","BIG",
    "SMALL","BIG","SMALL","BIG","SMALL","BIG","BIG","BIG","BIG","SMALL","SMALL","SMALL","SMALL","BIG","BIG",
    "SMALL","SMALL","BIG","BIG","SMALL","SMALL","BIG","BIG","BIG","SMALL","SMALL","BIG","BIG","SMALL","SMALL",
    "BIG","SMALL","BIG","SMALL","BIG"
]

def smart_predict(period: str, history=[]):
    index = int(period[-2:]) % len(prediction_pattern)
    return prediction_pattern[index]

def fetch_result():
    try:
        response = requests.post(API_URL, json={
            "pageSize": 10,
            "pageNo": 1,
            "typeId": 1,
            "language": 0,
            "random": "4a0522c6ecd8410496260e686be2a57c",
            "signature": "334B5E70A0C9B8918B0B15E517E2069C",
            "timestamp": int(time.time())
        })
        data = response.json()
        item = data.get("data", {}).get("list", [])[0]
        return item.get("issueNumber")
    except:
        return None

# Stylish fonts
def style_text(text):
    big_font = {
        "A": "𝗔", "B": "𝗕", "C": "𝗖", "D": "𝗗", "E": "𝗘", "F": "𝗙", "G": "𝗚", "H": "𝗛",
        "I": "𝗜", "J": "𝗝", "K": "𝗞", "L": "𝗟", "M": "𝗠", "N": "𝗡", "O": "𝗢", "P": "𝗣",
        "Q": "𝗤", "R": "𝗥", "S": "𝗦", "T": "𝗧", "U": "𝗨", "V": "𝗩", "W": "𝗪", "X": "𝗫",
        "Y": "𝗬", "Z": "𝗭"
    }
    return ''.join(big_font.get(c.upper(), c) for c in text)

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_period = fetch_result()
    if not current_period:
        await update.message.reply_text("API error. Try again later.")
        return

    next_period = str(int(current_period) + 1)
    prediction = smart_predict(next_period)
    styled = style_text(prediction)

    # Reply with period and prediction only
    reply = f"`{next_period}`   {styled} "

    await update.message.reply_text(reply, parse_mode="Markdown")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", predict))
    app.add_handler(CommandHandler("predict", predict))
    app.run_polling()