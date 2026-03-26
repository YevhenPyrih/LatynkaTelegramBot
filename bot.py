from telegram import Update
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, ContextTypes
from toLatinAlph import to_latin
from translations import translation_official, translation_yevhen, translation_custom

BOT_NAME = "@toLatinBot "

AWAIT_CHANGE_TRANSITION = 1

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    translation = context.chat_data.get('translation', translation_official)

    message = "Привіт! Я бот, створений для легкої конвертації української на латиницю!"
    translated = to_latin(message, translation)
    await update.message.reply_text(message + "\n\n" + translated)

async def free_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.chat_data["free_mode"] = True
    await update.message.reply_text("Увімкнуто вільний режим")

async def shackle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.chat_data["free_mode"] = False
    await update.message.reply_text("Вільний режим вимкнуто")

async def change_translation_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Оберіть тип:\n    1. Official\n    2.Creator's\n    3. Custom")
    return AWAIT_CHANGE_TRANSITION

async def process_change_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "1" in update.message.text or update.message.text.lower() == "official":
        context.chat_data['translation'] = translation_official
        await update.message.reply_text("Встановлено тип 'Official'")
    elif "2" in update.message.text or "creator" in update.message.text.lower():
        context.chat_data['translation'] = translation_yevhen
        await update.message.reply_text("Встановлено тип 'Creator's'")
    # elif "3" in update.message.text or "custom" in update.message.text.lower():
    #     context.chat_data['translation'] = translation_custom
    #     await update.message.reply_text("Встановлено тип 'Custom'")
    else:
        await update.message.reply_text("Невірний вибір. Будь ласка, оберіть зі списку: \n    1. Official\n    2.Creator's\n    3. Custom")
        return AWAIT_CHANGE_TRANSITION
    
    return ConversationHandler.END

async def cancel_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Зміна скасована")
    return ConversationHandler.END

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the incoming message and convert it to lowercase
    incoming_text = update.message.text
    translation = context.chat_data.get('translation', translation_official)
    free_mode = context.chat_data.get("free_mode", False)


    if free_mode:
    
        # Process the text letter by letter
        final_text = to_latin(incoming_text, translation)
    
        # Send the converted text back to the user
        await update.message.reply_text(final_text)
    else:
        if BOT_NAME in incoming_text:
            redacted_text = incoming_text.replace(BOT_NAME, "")
            final_text = to_latin(redacted_text, translation)
    
            # Send the converted text back to the user
            await update.message.reply_text(final_text)

def main():
    # Insert your BotFather token here
    application = Application.builder().token("8651073988:AAEH-Jo5JQ07YZEw4UF3eTFhKqJekNE2KZ0").build()

    # Tell the bot to listen for text messages (ignoring commands like /start)

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("free", free_command))
    application.add_handler(CommandHandler("shackle", shackle_command))

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("change_translation", change_translation_flow)],
        states={
            AWAIT_CHANGE_TRANSITION: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_change_reply)]
        },
        fallbacks=[CommandHandler("cancel", cancel_flow)]
    )

    application.add_handler(conversation_handler)

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running! Press Ctrl+C to stop.")
    
    # Start polling Telegram for new messages
    application.run_polling()

if __name__ == '__main__':
    main()