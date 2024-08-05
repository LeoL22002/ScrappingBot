import os
import time
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import telebot
from telebot import types
from dotenv import load_dotenv
import mysql.connector


#Vehiculos
vehicles={"description": "", "price": 0, "url": ""}
f_vehicles={"description": "", "price": 0, "url": ""}


# Variables de Parámetros
location = "miami"
category = "vehicles"
mark_model=""
days_listed = 1
minPrice = 0
maxPrice = 0
exact = False 


# https://www.facebook.com/marketplace/miami/search?daysSinceListed=1&minPrice=500&maxPrice=1000&query=honda%20civic&exact=false


# URL
base_url = f"https://www.facebook.com/marketplace/{location}/{category}?daysSinceListed={days_listed}"
url = f'{base_url}'

def GetMarketInfo(url):
    """
    url (str)
    Esta función obtiene la información de los vehículos del Facebook MarketPlace
    """
    global vehicles
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Activar el modo headless
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no-sandbox")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Activar el modo headless
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-logging")
    
    # Deshabilitar la carga de imágenes
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)



    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    time.sleep(5)  # Esperar a que la página cargue completamente...
    
    # Parsear el HTML
    html = browser.page_source
    browser.close()
    market_soup = soup(html, 'html.parser')
    
    # Extraer lista de títulos
    titles_div = market_soup.find_all('span', class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6")
    titles_list = [title.text.strip() for title in titles_div]

    # Extraer lista de precios
    prices_div = market_soup.find_all('span', class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u")
    prices_list = [price.text.strip() for price in prices_div]

    # Extraer lista de URLs
    urls_div = market_soup.find_all('a', class_="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lku1pv")
    urls_list = ["https://facebook.com" + url.get('href') for url in urls_div]

    vehicles = [{"description": description, "price": price, "url": url} for description, price, url in zip(titles_list, prices_list, urls_list)]
      

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Variables de entorno
TOKEN = os.getenv("MY_TOKEN")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Variables para manejar base de datos
db=None
cursor=None

# Datos del usuario
  
user_id = ""
user = ""
username=""


# Crear una instancia del bot de Telegram
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    global db,cursor,user_id,user,username
    user_id = message.from_user.id
    user = message.from_user.username
    username = message.from_user.first_name +" "+message.from_user.last_name

    db=connect_to_database()
    if(db is not None):
        cursor=db.cursor()
        user_start()
    
    bot.reply_to(message, 'Hola! Soy tu bot de Telegram. ¿En qué puedo ayudarte?')
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('Consultar Vehiculos')
    markup.add(btn1)
    bot.send_message(message.chat.id, 'Elige Una Opcion:', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Consultar Vehiculos')
def consult_vehicles(message):
    try:
        bot.send_message(message.chat.id, 'Buscando vehiculos, espere un momento... 🔎')
        # vehicles = GetMarketInfo(url)
        GetMarketInfo(url)
        ShowVehicles(message,vehicles)
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        markup = types.InlineKeyboardMarkup(row_width=2)
        search_btn = types.InlineKeyboardButton('Volver a buscar...', callback_data='search')
        markup.add(search_btn)
        bot.send_message(message.chat.id, 'Ocurrió un error buscando vehículos', reply_markup=markup)

def ShowVehicles(message,dict):
    for item in dict:
        info = f"{item['description']} - {item['price']} USD\nURL:{item['url']}"
        bot.send_message(message.chat.id, info, parse_mode="HTML")
    markup = types.InlineKeyboardMarkup(row_width=2)
    menu_buttons = [
            types.InlineKeyboardButton('Agregar Filtros ⚙', callback_data='add_filters'),
        ]
    markup.add(*menu_buttons)
    bot.send_message(message.chat.id, '¿Qué desea hacer?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'search':
        bot.send_message(call.message.chat.id, 'Buscando vehiculos...')
        bot.register_next_step_handler(call.message, consult_vehicles)
    elif call.data == 'add_filters':
        AddFilters(call)
    elif call.data == 'f_price':
        bot.send_message(call.message.chat.id, 'Introduzca el precio mínimo')
        bot.register_next_step_handler(call.message, get_min_price)
    elif call.data == 'f_markmodel':
        bot.send_message(call.message.chat.id, 'Introduzca la marca y el modelo')
        bot.register_next_step_handler(call.message,getMarkModel)





def AddFilters(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    filters_buttons = [
            types.InlineKeyboardButton('Precios 💵', callback_data='f_price'),
            types.InlineKeyboardButton('Marca y Modelo 🚙', callback_data='f_markmodel'),
            types.InlineKeyboardButton('Tienda 🛒', callback_data='market_type'),
        ]
    markup.add(*filters_buttons)
    bot.send_message(call.message.chat.id, 'Introduzca el filtro que desea aplicar', reply_markup=markup)

def get_min_price(message):
    global minPrice
    try:
        minPrice = int(message.text)
        bot.send_message(message.chat.id, 'Introduzca el precio máximo')
        bot.register_next_step_handler(message, get_max_price)
        
    except ValueError:
        bot.send_message(message.chat.id, 'Por favor, introduzca un número válido')
        bot.register_next_step_handler(message, get_min_price)

def get_max_price(message):
    global maxPrice,f_vehicles
    try:
        maxPrice = int(message.text)
        bot.send_message(message.chat.id, f'Filtros aplicados. Min: {minPrice} Max: {maxPrice}\nBuscando...')
        f_vehicles=[{"description":item['description'],"price":item['price'],"url":item['url']}
               for item in vehicles if int(item['price'].replace('$', '').replace('.', '').strip())
               >=minPrice and int(item['price'].replace('$', '').replace('.', '').strip())<=maxPrice]
        bot.send_message(message.chat.id,f'Se han encontrado {len(f_vehicles)} Vehiculos!')
        # print(f_vehicles)
        ShowVehicles(message=message,dict=f_vehicles)
    except ValueError:
        bot.send_message(message.chat.id, 'Por favor, introduzca un número válido')
        bot.register_next_step_handler(message, get_max_price)

def getMarkModel(message):
    global f_vehicles,vehicles
    f_vehicles=[{'description':item['description'],'price':item['price'],'url':item['url']}
                 for item in vehicles if message.text.lower() in item['description'].lower()]
    bot.send_message(message.chat.id,f'Se han encontrado {len(f_vehicles)} Vehiculos!')
    # print(f_vehicles)
    ShowVehicles(message=message,dict=f_vehicles)


def connect_to_database():
    try:
        # Conectar a la base de datos MySQL
        db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        # print("Conexión a la base de datos establecida correctamente.")
        return db
    except mysql.connector.Error as err:
        # print(f"Error al conectar a la base de datos: {err}")
        return None
    
def user_start():

    if(user_exists(_user_id=user_id)):
       try:
        cursor.execute('INSERT INTO users_sessions (user) VALUES (%s)',(user_id,))
       except  mysql.connector.Error as err:
           print(f"Error: {err}")
    else:
         try:
            cursor.execute('INSERT INTO users (id,user,username,status) VALUES (%s,%s,%s,%s)',(user_id,user,username,1))
         except mysql.connector.Error as err:
            print(f"Error: {err}")
    
    db.commit()
    
def user_exists(_user_id):
    try:
        query="SELECT * FROM users where id=%s limit 1"
        cursor.execute(query,(_user_id,))
        return cursor.fetchone() is not None
    except mysql.connector.Error as err:
        print(f"Error al verificar el usuario en la base de datos: {err}")
        return False
    

if __name__ == "__main__":
    print('\033[1m'+'\033[92m'+"Bot Iniciado")
    
    bot.polling(none_stop=True)


#TODO: Agregar nuevo filtro para la tienda en la que desea buscar
#TODO: Agregar nuevo filtro para la ubicacion