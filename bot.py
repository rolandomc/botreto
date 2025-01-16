import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import datetime

# Cargar variables de entorno
load_dotenv()

# Obtener el token del bot desde las variables de entorno
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


# Variables globales
ahorros = 0


# Función para enviar un número aleatorio diario
async def enviar_numero_diario(context: ContextTypes.DEFAULT_TYPE):
    global ahorros
    numero = random.randint(1, 365)
    ahorros += numero
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=f"Hoy debes ahorrar: {numero}.\nTotal acumulado: {ahorros}"
    )


# Función para agregar un número manualmente
async def agregar_manual(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ahorros
    try:
        numero = int(context.args[0])  # Capturar el número proporcionado por el usuario
        ahorros += numero
        await update.message.reply_text(f"Has agregado: {numero}.\nTotal acumulado: {ahorros}")
    except (IndexError, ValueError):
        await update.message.reply_text("Por favor, proporciona un número válido. Ejemplo: /agregar 100")


# Función para consultar el total acumulado
async def consultar_total(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Total acumulado: {ahorros}")


# Configurar comandos y tareas
def main():
    # Crear la aplicación del bot
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Registrar comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("agregar", agregar_manual))
    application.add_handler(CommandHandler("total", consultar_total))

    # Configurar tarea diaria
    hora_diaria = datetime.time(hour=8, minute=0)  # Cambia la hora si lo necesitas
    application.job_queue.run_daily(enviar_numero_diario, time=hora_diaria)

    # Iniciar el bot
    application.run_polling()


# Mensaje de bienvenida
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy tu bot de ahorro.\n\n"
                                    "Comandos disponibles:\n"
                                    "/agregar <número> - Agrega manualmente un monto al ahorro.\n"
                                    "/total - Consulta el total acumulado.\n")


if __name__ == "__main__":
    main()
