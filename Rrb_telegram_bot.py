from telegram import Update, Poll, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import logging

TOKEN = "8723743371:AAF9Ke4kUHI5m_rguWNPmEDBFhMdcavjbrA"

logging.basicConfig(level=logging.INFO)

QUESTIONS = [
    {"q": "Speed of train 180m long passing pole in 12s?", "opts": ["54 km/h","45 km/h","60 km/h","72 km/h"], "ans": 0, "exp": "15 m/s × 18/5 = 54 km/h"},
    {"q": "LCM of 12, 18, 24?", "opts": ["36","48","72","96"], "ans": 2, "exp": "LCM = 72"},
    {"q": "Powerhouse of the cell?", "opts": ["Nucleus","Ribosome","Chloroplast","Mitochondria"], "ans": 3, "exp": "Mitochondria = powerhouse"},
    {"q": "Battle of Plassey was fought in?", "opts": ["1764","1857","1757","1761"], "ans": 2, "exp": "June 23, 1757"},
    {"q": "Series: 3, 9, 27, 81, ?", "opts": ["162","200","243","270"], "ans": 2, "exp": "×3 each time = 243"},
]

idx = [0]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("▶ Quiz শুরু করো", callback_data="quiz")]]
    await update.message.reply_text("🚂 RRB Test Bot-এ স্বাগতম!", reply_markup=InlineKeyboardMarkup(kb))

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = QUESTIONS[idx[0] % len(QUESTIONS)]
    idx[0] += 1
    chat = update.effective_chat.id
    await context.bot.send_poll(chat_id=chat, question=q["q"], options=q["opts"],
        type=Poll.QUIZ, correct_option_id=q["ans"], is_anonymous=False,
        explanation=q["exp"], open_period=30)

async def btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await quiz(update, context)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("quiz", quiz))
app.add_handler(CallbackQueryHandler(btn))
app.run_polling()
