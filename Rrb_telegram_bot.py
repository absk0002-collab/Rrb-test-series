from telegram import Update, Poll, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, PollAnswerHandler

TOKEN = "8723743371:AAF9Ke4kUHI5m_rguWNPmEDBFhMdcavjbrA"

MATH = [
    {"q":"Speed of 180m train passing pole in 12s?","opts":["54 km/h","45 km/h","60 km/h","72 km/h"],"ans":0,"exp":"15 m/s x 18/5 = 54 km/h"},
    {"q":"LCM of 12, 18 and 24?","opts":["36","48","72","96"],"ans":2,"exp":"LCM = 72"},
    {"q":"SI on 5000 at 8% for 3 years?","opts":["1000","1200","1500","1800"],"ans":1,"exp":"SI = 1200"},
    {"q":"If 40% of number is 80, find 25%?","opts":["50","40","60","45"],"ans":0,"exp":"Number=200, 25%=50"},
    {"q":"CI on 10000 at 10% for 2 years?","opts":["2000","2100","2200","1900"],"ans":1,"exp":"CI=2100"},
]
REASONING = [
    {"q":"Odd one out: 64,125,216,343,730","opts":["512","343","730","64"],"ans":2,"exp":"730 is not a perfect cube"},
    {"q":"Series: 3,9,27,81,?","opts":["162","200","243","270"],"ans":2,"exp":"x3 each time = 243"},
    {"q":"PENCIL=QFODKM, PAPER=?","opts":["QBQFS","QCQFS","QAQFS","QAQFT"],"ans":0,"exp":"Each letter +1 = QBQFS"},
    {"q":"Book:Author :: Sculpture:?","opts":["Museum","Clay","Sculptor","Canvas"],"ans":2,"exp":"Sculptor creates Sculpture"},
    {"q":"Ravi 7th from left, 11th from right. Total?","opts":["16","17","18","19"],"ans":1,"exp":"7+11-1=17"},
]
GK = [
    {"q":"Battle of Plassey was fought in?","opts":["1764","1857","1757","1761"],"ans":2,"exp":"June 23, 1757"},
    {"q":"Powerhouse of the cell?","opts":["Nucleus","Ribosome","Chloroplast","Mitochondria"],"ans":3,"exp":"Mitochondria"},
    {"q":"RBI was established in?","opts":["1947","1945","1935","1950"],"ans":2,"exp":"1 April 1935"},
    {"q":"Neeraj Chopra won gold in?","opts":["Discus","Shot Put","Long Jump","Javelin"],"ans":3,"exp":"Javelin Throw 87.58m"},
    {"q":"Gas used in fire extinguishers?","opts":["Oxygen","Nitrogen","Carbon Dioxide","Hydrogen"],"ans":2,"exp":"CO2"},
]
scores = {}
polls = {}
idx = {"math":0,"reasoning":0,"gk":0}

MENU = ReplyKeyboardMarkup(
    [
        [KeyboardButton("📐 Math Quiz"), KeyboardButton("🧠 Reasoning Quiz")],
        [KeyboardButton("🌏 GK Quiz"), KeyboardButton("🎯 Random Quiz")],
        [KeyboardButton("📊 My Score"), KeyboardButton("🏆 Leaderboard")],
    ],
    resize_keyboard=True,
    persistent=True,
)

async def send_quiz(chat_id, section, context):
    bank = {"math":MATH,"reasoning":REASONING,"gk":GK}[section]
    q = bank[idx[section] % len(bank)]
    idx[section] += 1
    emoji = {"math":"📐","reasoning":"🧠","gk":"🌏"}[section]
    msg = await context.bot.send_poll(
        chat_id=chat_id,
        question=f"{emoji} {q['q']}",
        options=q["opts"],
        type=Poll.QUIZ,
        correct_option_id=q["ans"],
        is_anonymous=False,
        explanation=q["exp"],
        open_period=30,
    )
    polls[msg.poll.id] = {"ans":q["ans"],"exp":q["exp"]}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "RRB Test Bot-এ স্বাগতম! নিচের menu থেকে quiz শুরু করো",
        reply_markup=MENU
    )
    async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat = update.effective_chat.id
    user = update.effective_user
    uid = str(user.id)
    import random

    if text == "📐 Math Quiz":
        await send_quiz(chat, "math", context)
    elif text == "🧠 Reasoning Quiz":
        await send_quiz(chat, "reasoning", context)
    elif text == "🌏 GK Quiz":
        await send_quiz(chat, "gk", context)
    elif text == "🎯 Random Quiz":
        await send_quiz(chat, random.choice(["math","reasoning","gk"]), context)
    elif text == "📊 My Score":
        if uid not in scores or scores[uid]["total"] == 0:
            await update.message.reply_text("এখনো quiz দাওনি!", reply_markup=MENU)
        else:
            d = scores[uid]
            pct = round(d["correct"]/d["total"]*100)
            await update.message.reply_text(
                f"📊 {user.first_name} এর Score\n\n✅ সঠিক: {d['correct']}\n❌ ভুল: {d['wrong']}\n📝 মোট: {d['total']}\n🎯 {pct}%",
                reply_markup=MENU
            )
    elif text == "🏆 Leaderboard":
        if not scores:
            await update.message.reply_text("এখনো কেউ quiz দেয়নি!", reply_markup=MENU)
        else:
            top = sorted(scores.items(), key=lambda x: x[1]["correct"], reverse=True)[:5]
            text2 = "🏆 Leaderboard\n\n"
            medals = ["🥇","🥈","🥉","4.","5."]
            for i,(_, d) in enumerate(top):
                text2 += f"{medals[i]} {d['name']} — {d['correct']}/{d['total']}\n"
            await update.message.reply_text(text2, reply_markup=MENU)
    else:
        await update.message.reply_text("নিচের menu থেকে শুরু করো 👇", reply_markup=MENU)

async def poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.poll_answer
    user = answer.user
    uid = str(user.id)
    poll_id = answer.poll_id
    if poll_id not in polls:
        return
    selected = answer.option_ids[0] if answer.option_ids else -1
    correct = selected == polls[poll_id]["ans"]
    if uid not in scores:
        scores[uid] = {"name":user.first_name,"correct":0,"wrong":0,"total":0}
    scores[uid]["total"] += 1
    if correct:
        scores[uid]["correct"] += 1
    else:
        scores[uid]["wrong"] += 1
    try:
        await context.bot.send_message(
            chat_id=user.id,
            text=f"{'✅ সঠিক!' if correct else '❌ ভুল!'}\n\n💡 {polls[poll_id]['exp']}\n\n📊 Score: {scores[uid]['correct']}/{scores[uid]['total']}"
        )
    except:
        pass

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(PollAnswerHandler(poll_answer))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()
