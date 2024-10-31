import requests
import json
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self,base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        self.LANGUAGE = "en-US,en;q=0.5"

    def setup_session(self):
        self.session.headers['User-Agent'] = self.USER_AGENT
        self.session.headers['Accept-Language'] = self.LANGUAGE
        self.session.headers['Content-Language'] = self.LANGUAGE

    def fetch_html_content(self, pdf_name):
        self.setup_session()
        response = self.session.get(f"{self.base_url}/{pdf_name}")
        response.raise_for_status()
        return response.text

