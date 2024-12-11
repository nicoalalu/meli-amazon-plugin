import requests
from bs4 import BeautifulSoup
import logging

def scrape_publication(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print(f"Intentando acceder a: {url}")
        response = requests.get(url, headers=headers)
        print(f"Código de respuesta: {response.status_code}")
        
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscar el título con diferentes selectores
        title_selectors = [
            'h1.ui-pdp-title',
            'h1[class*="ui-pdp"]',
            'h1.item-title',
            'div.ui-pdp-title'
        ]
        
        publication_name = None
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                publication_name = element.text.strip()
                print(f"Título encontrado: {publication_name}")
                break
        
        # Buscar el precio con diferentes selectores
        price_selectors = [
            'andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact',
            'span.price-tag-fraction',
            'meta[itemprop="price"]',
            'span[class*="price"]'
        ]
        
        price = None
        for selector in price_selectors:
            element = soup.select_one(selector)
            if element:
                if selector == 'meta[itemprop="price"]':
                    price = element.get('content')
                else:
                    price = element.text.strip()
                print(f"Precio encontrado: {price}")
                break
        
        if not publication_name or not price:
            print("No se encontró título o precio")
            return None
            
        return [publication_name, publication_name, price]
        
    except Exception as e:
        print(f"Error durante el scraping: {str(e)}")
        return None
