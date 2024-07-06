from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import time
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

# Print the extracted data
for vehicle in vehicles:
    print(vehicle)

# input("Press ENTER to exit\n")

























#ANTIGUA FUNCION DE GETDATA
    # browser= Browser('chrome') #Creating the chrome browser instance
    # browser.visit(url)
    # time.sleep(5) #Waiting for the page to load completely...
    # #Parse HTML
    # html=browser.html
    # browser.quit()
    # market_soup=soup(html,'html.parser')



    # #Extracting Titles List...
    # titles_div=market_soup.find_all('span',class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6")
    # titles_list=[title.text.strip() for title in titles_div]


    # #Extracting Prices List...
    # prices_div=market_soup.find_all('span',class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u")
    # prices_list=[price.text.strip() for price in prices_div]



    # #Extracting URLs List...
    # urls_div=market_soup.find_all('a',class_="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lku1pv")
    # urls_list=[ "https://facebook.com"+url.get('href') for url in urls_div]

    # vehicles = [{"description": description, "price": price, "url": url} for description, price, url in zip(titles_list, prices_list, urls_list)]
    # return vehicles