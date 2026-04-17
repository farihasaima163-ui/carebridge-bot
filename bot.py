from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

import os
BOT_TOKEN = os.environ.get("8515404096:AAG8d1-vCfgSfQZgncdSoc2xNCfYxDjds-4")

# Add your 5 admin IDs here
ADMIN_IDS = [6687917006, 7612005461, 5281179398, 1865092522, 6281438127, 8579277904]

# START MESSAGE
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome. Send your message. Admins will reply soon."
    )

# USER MESSAGE → SEND TO ALL ADMINS
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    message = f"""
📩 NEW MESSAGE

👤 Name: {user.first_name}
🔗 Username: @{user.username}
🆔 User ID: {user.id}

💬 Message:
{text}

Reply using:
/reply {user.id} your message
"""

    for admin in ADMIN_IDS:
        await context.bot.send_message(chat_id=admin, text=message)

# ADMIN REPLY → SEND TO USER
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin = update.message.from_user

    if admin.id not in ADMIN_IDS:
        return

    user_id = int(context.args[0])
    reply_text = " ".join(context.args[1:])

    # send to user
    await context.bot.send_message(
        chat_id=user_id,
        text=f"💬 Admin reply:\n{reply_text}"
    )

    # notify all admins
    for admin_id in ADMIN_IDS:
        await context.bot.send_message(
            chat_id=admin_id,
            text=f"↩️ Reply sent to {user_id}:\n{reply_text}"
        )

# BUILD APP
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
app.add_handler(CommandHandler("reply", reply))

app.run_polling()