import os
from dotenv import load_dotenv
from telebot import types
import telebot
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import time
import prettytable as pt


browser= Browser('chrome') #Creating the chrome browser instance

#Parameters Variables
location="miami"
category="vehicles"
# mark="Honda"
# model="Civic"
days_listed=7
minPrice=100
maxPrice=5000
# itemCondition="used_like_new" #Expects: new, used_fair, used_like_new, used_good
exact=False 

#URL
base_url=f"https://www.facebook.com/marketplace/{location}/{category}?"
url=f'{base_url}minPrice={minPrice}&maxPrice={maxPrice}&daysSinceListed={days_listed}&exact={exact}'
# print(url)
browser.visit(url)
time.sleep(5) #Waiting for the page to load completely...
#Parse HTML
html=browser.html
browser.quit()
market_soup=soup(html,'html.parser')



#Extracting Titles List...
titles_div=market_soup.find_all('span',class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6")
titles_list=[title.text.strip() for title in titles_div]


#Extracting Prices List...
prices_div=market_soup.find_all('span',class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u")
prices_list=[price.text.strip() for price in prices_div]



#Extracting URLs List...
urls_div=market_soup.find_all('a',class_="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lku1pv")
urls_list=[ "https://facebook.com"+url.get('href') for url in urls_div]

vehicles = [{"description": description, "price": price, "url": url} for description, price, url in zip(titles_list, prices_list, urls_list)]



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
    info=""
    for vehicle in vehicles[:5]:
        info+=f"{vehicle['url']}\n\n"
    #print(tabla_str)
    # Enviar el mensaje con la tabla
    bot.send_message(message.chat.id, info,parse_mode="HTML")

    
    
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


