import os
import logging
import sys
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
mode = os.getenv("MODE")

if mode == 'dev':
    # creamos acceso (desarollo)
    def run(application):
        application.run_polling()

elif mode == 'prod':
    # creamos acceso (produccion)
    def run(application):
        PORT = int(os.environ.get("PORT", "8443"))
        RENDER_APP_NAME = os.environ.get('RENDER_APP_NAME')
        # weebhook check https://api.telegram.org/bot<your_bot_token>/getWebhookInfo
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            #secret_token=TOKEN,
            webhook_url=f"https://{RENDER_APP_NAME}.onrender.com/"
        )
else: 
    logger.info('no se especifico el mode')
    sys.exit()

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
    
    run(application)