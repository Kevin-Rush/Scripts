import requests
from bs4 import BeautifulSoup

def search_urls(urls, keywords):
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()

        for keyword in keywords:
            if keyword in text:
                print(f"Keyword '{keyword}' found in URL: {url}")

# Example usage
urls = ['https://www.mcvts.org', 'https://www.ocean.edu']

keywords = ['python', 'web scraping']

search_urls(urls, keywords)