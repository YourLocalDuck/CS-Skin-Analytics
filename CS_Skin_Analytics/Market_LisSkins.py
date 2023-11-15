import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth

# No API documentation, reverse engineering not possible. Probably use BeatifulSoup to scrape the website.
class Market_LisSkins():
    def __init__(self):
        self.url = "https://lis-skins.ru/market/cs2/"
        options = webdriver.ChromeOptions()
        service = webdriver.ChromeService(executable_path='./home/prince/chromedriver-linux64/chromedriver')
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(service=service, options=options)
        self.soup = self.get_soup()
        print(self.soup)
        
    def get_soup(self):
        #response = requests.get(self.url)
        self.driver.get(self.url)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        return soup
    
    def get_items(self):
        items = []
        for item in self.soup.find_all('div', class_='market-item'):
            name = item.find('div', class_='market-item__name').text.strip()
            price = item.find('div', class_='market-item__price').text.strip()
            items.append({'name': name, 'price': price})
        return items
