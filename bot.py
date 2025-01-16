import os
import random
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
import schedule
import time
import threading

# Cargar variables de entorno
load_dotenv()

# Obtener el token del bot desde las variables de entorno
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # Opcional si quieres enviar mensajes a un chat específico

# Variables globales
ahorros = 0

# Función para enviar un número aleatorio diario
def enviar_numero_diario(context: CallbackContext):
    global ahorros
    numero = random.randint(1, 365)
    ahorros += numero
    context.bot.send_message(chat_id=CHAT_ID or context.job.context, 
                             text=f"Hoy debes ahorrar: {numero}.\nTotal acumulado: {ahorros}")

# Función para agregar un número manualmente
def agregar_manual(update: Update, context: CallbackContext):
    global ahorros
    try:
        numero = int(context.args[0])  # Capturar el número proporcionado por el usuario
        ahorros += numero
        update.message.reply_text(f"Has agregado: {numero}.\nTotal acumulado: {ahorros}")
    except (IndexError, ValueError):
        update.message.reply_text("Por favor, proporciona un número válido. Ejemplo: /agregar 100")

# Función para consultar el total acumulado
def consultar_total(update: Update, context: CallbackContext):
    update.message.reply_text(f"Total acumulado: {ahorros}")

# Configurar los handlers del bot
def main():
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    # Comandos
    dispatcher.add_handler(CommandHandler("start", lambda update, _: update.message.reply_text("¡Hola! Soy tu bot de ahorro.")))
    dispatcher.add_handler(CommandHandler("agregar", agregar_manual))
    dispatcher.add_handler(CommandHandler("total", consultar_total))

    # Configurar envío diario del número aleatorio
    def enviar_diario():
        schedule.every().day.at("08:00").do(lambda: enviar_numero_diario(updater.bot))

        while True:
            schedule.run_pending()
            time.sleep(1)

    # Crear un hilo para la tarea diaria
    threading.Thread(target=enviar_diario, daemon=True).start()

    # Iniciar el bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
