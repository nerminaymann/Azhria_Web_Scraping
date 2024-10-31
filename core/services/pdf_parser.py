from bs4 import BeautifulSoup

from .web_scraper_service import WebScraper


class PDFParser(WebScraper):
    def __init__(self, base_url, pdf_name):
        super().__init__(base_url)
        self.pdf_name = pdf_name
        self.html_content = self.fetch_html_content(pdf_name)
        self.soup = BeautifulSoup(self.html_content, 'html.parser')

    def parse_pdf_files(self):
        selected_menue_pdf_files_div = self.soup.find('div', class_='selected-menu')
        content_pdf_files = selected_menue_pdf_files_div.find_all('div', class_='content')
        pdf_files_list = []
        for pdf_file in content_pdf_files:
            parsed_pdf_file = self.download_pdf_file(pdf_file)
            if parsed_pdf_file:
                pdf_files_list.append(parsed_pdf_file)
        return pdf_files_list

    def download_pdf_file(self, pdf_file):
        pdf_file_link = pdf_file.find('a')['href']
        pdf_file_name = pdf_file_link.find('p',class_='item-title').text
        if pdf_file_link and pdf_file_name:
            pass









