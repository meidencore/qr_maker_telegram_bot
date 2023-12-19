import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import qrcode

# Configurar Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
)
logger = logging.getLogger()

# Solicitar TOKEN
TOKEN = os.getenv("TOKEN")


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'El usuario {update.effective_user.username} con el '
                f'id:{update.effective_user.id} ha iniciado una conversacion')
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hola, Si me envias un texto, generaré un QR y te lo enviaré"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text
    message_id = update.effective_message.id
    chat_id = update.effective_chat.id
    img = qrcode.make(text)
    f = open("output.png", "wb")
    img.save(f)
    f.close()
    await context.bot.send_photo(chat_id=chat_id, photo=open("output.png", "rb"), reply_to_message_id=message_id)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    # declaramos los handlers
    start_handler = CommandHandler("start", cmd_start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    # agregamos los handlers
    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()
