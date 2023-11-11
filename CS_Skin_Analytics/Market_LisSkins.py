import requests
from bs4 import BeautifulSoup

# No API documentation, reverse engineering not possible. Probably use BeatifulSoup to scrape the website.
class Market_LisSkins():
    def __init__(self):
        super().__init__()
        self.name = "LisSkins"
        self.url = "https://lis-skins.ru/market/cs2/"
        self.soup = self.get_soup()
        
    def get_soup(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    
    def get_items(self):
        items = []
        for item in self.soup.find_all('div', class_='market-item'):
            name = item.find('div', class_='market-item__name').text.strip()
            price = item.find('div', class_='market-item__price').text.strip()
            items.append({'name': name, 'price': price})
        return items
