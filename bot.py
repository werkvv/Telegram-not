from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8727235182:AAFYIfiWz9sdlL7xFs_EX5gbI0i_HKY8kzE"
OWNER_ID = 123456789  # ← TU wpisz swój Telegram ID

warns = {}

async def is_admin(update, context):
    member = await context.bot.get_chat_member(
        update.effective_chat.id,
        update.effective_user.id
    )
    return member.status in ["administrator", "creator"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot admina działa 🔥")

# WARN SYSTEM
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return

    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        user_id = user.id

        warns[user_id] = warns.get(user_id, 0) + 1

        if warns[user_id] >= 3:
            await context.bot.ban_chat_member(update.effective_chat.id, user_id)
            await update.message.reply_text(f"{user.first_name} dostał bana za 3 warny 🔨")
            warns[user_id] = 0
        else:
            await update.message.reply_text(f"{user.first_name} ma {warns[user_id]}/3 warnów ⚠️")

# KICK
async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await context.bot.ban_chat_member(update.effective_chat.id, user_id)
        await context.bot.unban_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text("Wyrzucono użytkownika 🚫")

# BAN
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await context.bot.ban_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text("Zbanowano użytkownika 🔨")

# UNBAN
async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return

    if context.args:
        user_id = int(context.args[0])
        await context.bot.unban_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text("Odbanowano użytkownika 🔓")

# MUTE
from telegram import ChatPermissions

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id

      from datetime import datetime, timedelta
import re

args = context.args

duration = timedelta(hours=1)

if args:
    match = re.match(r"(\d+)([mhd])", args[0])
    if match:
        value, unit = match.groups()

        if unit == "m":
            duration = timedelta(minutes=int(value))
        elif unit == "h":
            duration = timedelta(hours=int(value))
        elif unit == "d":
            duration = timedelta(days=int(value))

until_date = datetime.now() + duration

await context.bot.restrict_chat_member(
    chat_id=update.effective_chat.id,
    user_id=user_id,
    permissions=ChatPermissions(can_send_messages=False),
    until_date=until_date
)

        await update.message.reply_text("Wyciszono użytkownika 🔇")


async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id

        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_send_audios=True,
                can_send_documents=True,
                can_send_photos=True,
                can_send_videos=True,
                can_send_video_notes=True,
                can_send_voice_notes=True
            )
        )

        await update.message.reply_text("Odmutowano użytkownika 🔊")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("warn", warn))
app.add_handler(CommandHandler("kick", kick))
app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("unban", unban))
app.add_handler(CommandHandler("mute", mute))
app.add_handler(CommandHandler("unmute", unmute))

app.run_polling()
