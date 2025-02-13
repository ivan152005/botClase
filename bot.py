#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging

from openai import OpenAI
from telegram import ForceReply, Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

TOKEN = "7582374391:AAEYVIaPhCqt7Hxb3QMeS2SW0ynF6FMNOJ8"
lista_nombres = {'Diana', 'Alejandro','Daniel', 'gg'}

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

async def bye(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await update.message.reply_text("Adios que tengas buena tarde")


# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Procesa los mensajes y responde con IA si no es un nombre conocido."""
#     texto = update.message.text.strip()  # Limpia espacios en blanco
#
#     if not texto:  # Evita mensajes vacíos
#         await update.message.reply_text("Parece que enviaste un mensaje vacío. Intenta de nuevo.")
#         return
#
#     if texto in lista_nombres:
#         await update.message.reply_text('Estás dentro de la clase.')
#
#     elif texto == "¿Cómo fue la toma de Granada?":  # Verifica la pregunta específica
#         try:
#             completion = client.chat.completions.create(
#                 model="deepseek/deepseek-r1:free",
#                 messages=[{"role": "user", "content": texto}]
#             )
#
#             # Verificar si la respuesta tiene contenido antes de enviarla
#             if completion and completion.choices and completion.choices[0].message.content:
#                 respuesta_ai = completion.choices[0].message.content.strip()
#                 mensaje_final = respuesta_ai + "\n\n La toma de Granada marcó el fin de la Reconquista en 1492."
#                 await update.message.reply_text(mensaje_final)
#             else:
#                 await update.message.reply_text("No se pudo obtener una respuesta válida de la IA.")
#
#         except Exception as e:
#             logger.error(f"Error al obtener respuesta de OpenAI: {e}")
#             await update.message.reply_text("Hubo un problema con la IA al responder sobre la toma de Granada.")
#
#     else:  # Para cualquier otro mensaje, responde con la IA normalmente
#         try:
#             completion = client.chat.completions.create(
#                 model="deepseek/deepseek-r1:free",
#                 messages=[{"role": "user", "content": texto}]
#             )
#
#             # Verificar si la respuesta tiene contenido antes de enviarla
#             if completion and completion.choices and completion.choices[0].message.content:
#                 respuesta_ai = completion.choices[0].message.content.strip()
#                 await update.message.reply_text(respuesta_ai)
#             else:
#                 await update.message.reply_text("No se pudo obtener una respuesta válida de la IA.")
#
#         except Exception as e:
#             logger.error(f"Error al obtener respuesta de OpenAI: {e}")
#             await update.message.reply_text("No te reconozco y hubo un problema con la IA.")

async def menu(update: Update, context: CallbackContext) -> None:
    keyboard = [["Coche", "Moto"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("¿Qué vehículo necesita un seguro?", reply_markup=reply_markup)

async def option_selected(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    keyboard = []
    print(text)

    if text == "Coche":
        keyboard = [["< 120cv", "Entre 121cv y 200cv", "> 201cv"]]
        if text == "< 120cv":
            await update.message.reply_text("Perfecto")
            return
        elif text == "Entre 121cv y 200cv":
            await update.message.reply_text("Perfecto")
        elif text == "> 201cv":
            keyboard = [["Emisión 30 g", "Emisión 50 g"]]
            await update.message.reply_text("Perfecto")

    elif text == "Moto":
        keyboard = [["> 50cc", "< 50cc"]]
        await update.message.reply_text("Perfecto")
        if text == "> 50cc":
            keyboard = [["Permiso A1", "Permiso A2"]]
            await update.message.reply_text("Perfecto")
        elif text == "< 50cc":
            keyboard = [["> 18 años"]]
            await update.message.reply_text("Perfecto")
    else:
        await update.message.reply_text("No la encuentro")

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard= True, one_time_keyboard=True)
    await update.message.reply_text("Selecciona una subopción", reply_markup=reply_markup)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("contratar", menu))
    application.add_handler(CommandHandler("bye", bye))

    # Manejador para la primera selección
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, option_selected))

    # on non command i.e message - echo the message on Telegram
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()