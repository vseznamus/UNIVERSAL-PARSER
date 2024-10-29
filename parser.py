
import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from urllib.parse import urljoin
import logging

class UniversalParser:
    def __init__(self, base_url, output_file='parsed_data.csv'):
        self.base_url = base_url
        self.output_file = output_file
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def get_page(self, url):
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            self.logger.error(f"Error fetching page {url}: {str(e)}")
            return None

    def parse_elements(self, soup, selectors):
       
        result = {}
        for key, selector in selectors.items():
            try:
                element = soup.select_one(selector)
                result[key] = element.text.strip() if element else ''
            except Exception as e:
                self.logger.error(f"Error parsing {key}: {str(e)}")
                result[key] = ''
        return result

    def save_to_csv(self, data):
        try:
            with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
                if data:
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
            self.logger.info(f"Data saved to {self.output_file}")
        except Exception as e:
            self.logger.error(f"Error saving data: {str(e)}")

    def parse_site(self, selectors, pages=None, delay=(1, 3)):
        
        all_data = []
        current_page = 1

        while pages is None or current_page <= pages:
            url = f"{self.base_url}/page/{current_page}" if current_page > 1 else self.base_url
            self.logger.info(f"Parsing page {current_page}: {url}")

            html = self.get_page(url)
            if not html:
                break

            soup = BeautifulSoup(html, 'html.parser')
            page_data = self.parse_elements(soup, selectors)
            
            if not page_data:
                break

            all_data.append(page_data)
            
            
            time.sleep(random.uniform(delay[0], delay[1]))
            current_page += 1

        self.save_to_csv(all_data)
        return all_data
    
if __name__ == "__main__":
    parser = UniversalParser('https://freetp.org/polnyy-spisok-igr-na-sayte.html')
    selectors = {
        'list': '.mainside',
    }
    parser.parse_site(selectors)

"""
Инструкция по использованию парсера:

1. Создание экземпляра парсера:
parser = UniversalParser('https://example.com')

2. Определение селекторов для нужных элементов:
selectors = {
    'title': '.product-title',  # CSS селектор для заголовка
    'price': '.product-price',  # CSS селектор для цены
    'description': '.product-description'  # CSS селектор для описания
}

3. Запуск парсинга:
# Парсинг определенного количества страниц
data = parser.parse_site(selectors, pages=5)

# Парсинг всех доступных страниц
data = parser.parse_site(selectors)

4. Примеры использования:

# Пример парсинга интернет-магазина
shop_parser = UniversalParser('https://shop.com', 'products.csv')
shop_selectors = {
    'name': '.product-name',
    'price': '.product-price',
    'availability': '.stock-status'
}
shop_parser.parse_site(shop_selectors, pages=10)

# Пример парсинга новостного сайта
news_parser = UniversalParser('https://news.com', 'news.csv')
news_selectors = {
    'headline': '.article-headline',
    'date': '.publish-date',
    'content': '.article-content'
}
news_parser.parse_site(news_selectors)

Важные замечания:
- Перед использованием проверьте политику robots.txt сайта
- Установите адекватные задержки между запросами
- Убедитесь, что CSS селекторы корректны для конкретного сайта
- При необходимости настройте прокси и User-Agent
"""
