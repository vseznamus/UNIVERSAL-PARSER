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
