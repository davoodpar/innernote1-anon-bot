import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import logging

# فعال کردن لاگ‌ها
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# بارگذاری توکن و کانال از config.json
with open("config.json") as f:
    config = json.load(f)

BOT_TOKEN = config["BOT_TOKEN"]
CHANNEL_USERNAME = config["CHANNEL_USERNAME"]

# دیکشنری برای ذخیره لینک اختصاصی کاربرا
user_links = {}

# دستور استارت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or str(user_id)

    # چک عضویت در کانال
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            # دادن لینک اختصاصی
            user_link = f"t.me/{context.bot.username}?start={user_id}"
            user_links[user_id] = user_link
            await update.message.reply_text(f"لینک اختصاصی شما: {user_link}")
        else:
            await update.message.reply_text(f"ابتدا باید عضو کانال {CHANNEL_USERNAME} شوید.")
    except:
        await update.message.reply_text(f"ابتدا باید عضو کانال {CHANNEL_USERNAME} شوید.")

# دریافت پیام ناشناس
async def receive_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    # پیدا کردن صاحب لینک
    if update.message.reply_to_message and update.message.reply_to_message.text:
        # برای مرحله بعد پاسخ ناشناس اضافه می‌کنیم
        await update.message.reply_text("پیام شما ثبت شد!")
    else:
        await update.message.reply_text("ابتدا لینک اختصاصی دریافت کنید و بعد پیام بدهید.")

# اجرای ربات
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), receive_message))

print("Bot is running...")
app.run_polling()
