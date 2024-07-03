import os
from dotenv import load_dotenv
from telebot import types
import telebot


# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener el token de Telegram desde la variable de entorno
TOKEN = os.getenv("MY_TOKEN")

# Crear una instancia del bot de Telegram
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])

# Función para el comando /start
def start_command(message):
    bot.reply_to(message,'Hola! Soy tu bot de Telegram. ¿En qué puedo ayudarte?')
    markup=types.ReplyKeyboardMarkup(row_width=2)
    btn1=types.KeyboardButton('Consultar Vehiculos')
    markup.add(btn1)
    bot.send_message(message.chat.id,'Elige Una Opcion:',reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Consultar Vehiculos')

def consult_vehicles(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    filter_btn = types.InlineKeyboardButton('Agregar Filtros ⚙', callback_data='add_filters')
    show_more_btn = types.InlineKeyboardButton('Mostrar Más Vehiculos 🚗', callback_data='show_more')
    markup.add(filter_btn, show_more_btn)
    bot.send_message(message.chat.id, 'Buscando vehículos...', reply_markup=markup)


@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    markup=types.ReplyKeyboardMarkup(row_width=2)
    if call.data=='add_filters':
        bot.send_message(call.message.chat.id,'Buscando filtros...')
    elif call.data=='show_more':
        bot.send_message(call.message.chat.id,'Buscando mas vehiculos...')

if __name__=="__main__":
    bot.polling(none_stop=True)