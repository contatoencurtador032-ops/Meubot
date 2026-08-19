from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)
import asyncio

# ====================== CONFIGURAÇÃO ======================
TOKEN = "8517238996:AAFN-7HxxJ0opRQdlfUpS-nWpNTwaIjzf4U"   # ← Coloque seu token aqui de novo

WAITING_PHOTO = 1

def main_menu():
    keyboard = [
        [InlineKeyboardButton("🎬 Image to Video", callback_data="cat_video")],
        [InlineKeyboardButton("⚡ Xray", callback_data="cat_xray"),
         InlineKeyboardButton("💜 Image to Nude", callback_data="cat_nude")],
        [InlineKeyboardButton("👗 Sexy", callback_data="cat_sexy")],
        [InlineKeyboardButton("🔥 Nudes", callback_data="cat_nudes")],
        [InlineKeyboardButton("💋 Sex Scenes", callback_data="cat_sex")],
        [InlineKeyboardButton("🦶 Kinks", callback_data="cat_kinks")],
        [InlineKeyboardButton("✋ Handjobs & Facials", callback_data="cat_handjobs")],
        [InlineKeyboardButton("💎 Meus Créditos", callback_data="credits")],
    ]
    return InlineKeyboardMarkup(keyboard)

def sexy_menu():
    keyboard = [
        [InlineKeyboardButton("👙 Bikini", callback_data="style_bikini"),
         InlineKeyboardButton("Lingerie", callback_data="style_lingerie")],
        [InlineKeyboardButton("⬅️ Voltar", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def nudes_menu():
    keyboard = [
        [InlineKeyboardButton("🍒 Breasts", callback_data="style_breasts"),
         InlineKeyboardButton("🛏️ Bed", callback_data="style_bed")],
        [InlineKeyboardButton("🚿 Shower", callback_data="style_shower"),
         InlineKeyboardButton("🛁 Bath", callback_data="style_bath")],
        [InlineKeyboardButton("🤰 Pregnant", callback_data="style_pregnant"),
         InlineKeyboardButton("Legs Spread", callback_data="style_legs")],
        [InlineKeyboardButton("⬅️ Voltar", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def sex_scenes_menu():
    keyboard = [
        [InlineKeyboardButton("💋 Kissing", callback_data="style_kissing"),
         InlineKeyboardButton("🍆 Dildo", callback_data="style_dildo")],
        [InlineKeyboardButton("👄 Fellatio", callback_data="style_fellatio"),
         InlineKeyboardButton("Prone Bone", callback_data="style_prone")],
        [InlineKeyboardButton("Cowgirl", callback_data="style_cowgirl")],
        [InlineKeyboardButton("⬅️ Voltar", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def kinks_menu():
    keyboard = [
        [InlineKeyboardButton("Feet Up", callback_data="style_feet"),
         InlineKeyboardButton("Armpits", callback_data="style_armpits")],
        [InlineKeyboardButton("Latex", callback_data="style_latex"),
         InlineKeyboardButton("Peeing", callback_data="style_peeing")],
        [InlineKeyboardButton("⬅️ Voltar", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def handjobs_menu():
    keyboard = [
        [InlineKeyboardButton("Handjob", callback_data="style_handjob"),
         InlineKeyboardButton("Titjob", callback_data="style_titjob")],
        [InlineKeyboardButton("Deepthroat", callback_data="style_deepthroat"),
         InlineKeyboardButton("Gangbang", callback_data="style_gangbang")],
        [InlineKeyboardButton("Blowjob", callback_data="style_blowjob"),
         InlineKeyboardButton("Cumshot", callback_data="style_cumshot")],
        [InlineKeyboardButton("⬅️ Voltar", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 *OpenGoon Bot*\n\nEscolha uma opção:",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back_main":
        await query.edit_message_text(
            "🔥 *OpenGoon Bot*\n\nEscolha uma opção:",
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )
        return ConversationHandler.END

    if data == "credits":
        await query.edit_message_text("💎 Sistema de créditos ainda não configurado.")
        return ConversationHandler.END

    if data in ["cat_video", "cat_xray", "cat_nude"]:
        context.user_data["style"] = data
        await query.edit_message_text("📸 Envie a foto agora:")
        return WAITING_PHOTO

    if data == "cat_sexy":
        await query.edit_message_text("Escolha o estilo:", reply_markup=sexy_menu())
    elif data == "cat_nudes":
        await query.edit_message_text("Escolha o estilo:", reply_markup=nudes_menu())
    elif data == "cat_sex":
        await query.edit_message_text("Escolha o estilo:", reply_markup=sex_scenes_menu())
    elif data == "cat_kinks":
        await query.edit_message_text("Escolha o estilo:", reply_markup=kinks_menu())
    elif data == "cat_handjobs":
        await query.edit_message_text("Escolha o estilo:", reply_markup=handjobs_menu())

    if data.startswith("style_"):
        context.user_data["style"] = data
        await query.edit_message_text("📸 Envie a foto agora:")
        return WAITING_PHOTO

async def receive_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        await update.message.reply_text("Por favor, envie uma foto.")
        return WAITING_PHOTO

    style = context.user_data.get("style", "desconhecido")
    await update.message.reply_text(f"⏳ Gerando com o estilo: `{style}`\nAguarde...")

    await update.message.reply_text(
        f"✅ Foto recebida!\nEstilo: `{style}`\n\n"
        "Aqui depois vai aparecer o resultado da API."
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelado.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler)],
        states={
            WAITING_PHOTO: [MessageHandler(filters.PHOTO, receive_photo)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot iniciado com sucesso!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
