from unittest import result
from urllib import response
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests

#PATH = 
search_keyword = input('Search: ')
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#use cd command to discord_bot before use
driver = webdriver.Chrome('chromedriver.exe',options=options)

#URL TEMPLATE
def get_url(search_word):
    template = 'https://www.youtube.com/results?search_query={}'
    search_word = search_word.replace(' ','+')
    return template.format(search_word)

#OPEN URL
url = get_url(search_keyword)
driver.get(url)

#YOUTUBE_web = BeautifulSoup(driver.page_source,'html.parser'
YOUTUBE_web = BeautifulSoup(driver.page_source,'html.parser')
#images = YOUTUBE_web.find_all('https://i.ytimg.com/vi/')
http = YOUTUBE_web.find_all('yt-img-shadow',href=True)

for link in http:
    print(link)

    
