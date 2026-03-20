from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8727235182:AAG5HtJZuiV8PciG_MeZhAfgKTcKnYfqkFo"
OWNER_ID = 123456789  # ← TU wpisz swój Telegram ID

warns = {}

def is_admin(user_id):
    return user_id == OWNER_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot admina działa 🔥")

# WARN SYSTEM
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
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
    if not is_admin(update.effective_user.id):
        return

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await context.bot.ban_chat_member(update.effective_chat.id, user_id)
        await context.bot.unban_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text("Wyrzucono użytkownika 🚫")

# BAN
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await context.bot.ban_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text("Zbanowano użytkownika 🔨")

# UNBAN
async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    if context.args:
        user_id = int(context.args[0])
        await context.bot.unban_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text("Odbanowano użytkownika 🔓")

# MUTE
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_id,
            permissions={}
        )
        await update.message.reply_text("Wyciszono użytkownika 🔇")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("warn", warn))
app.add_handler(CommandHandler("kick", kick))
app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("unban", unban))
app.add_handler(CommandHandler("mute", mute))

app.run_polling()