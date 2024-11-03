import os
from bs4 import BeautifulSoup
from django.core.files import File
from Azhria_Web_Scraping import settings
from .web_scraper_service import WebScraper
from ..models import PDF


class PDFParser(WebScraper):
    def __init__(self, base_url, pdf_name):
        super().__init__(base_url)
        self.pdf_name = pdf_name
        self.html_content = self.fetch_html_content(pdf_name)
        self.soup = BeautifulSoup(self.html_content, 'html.parser')

    def parse_pdf_files(self):
        selected_menue_pdf_files_div = self.soup.find('div', class_='selected-menu')
        if not selected_menue_pdf_files_div:
            print("No selected menu div found.")
            return []

        content_pdf_files = selected_menue_pdf_files_div.find_all('div', class_='content')
        pdf_files_list = []

        for pdf_file in content_pdf_files:
            parsed_pdf_file = self.extract_pdf_file_info(pdf_file)
            if parsed_pdf_file:
                pdf_files_list.append(parsed_pdf_file)

        return pdf_files_list

    def extract_pdf_file_info(self, pdf_file):
        # pdf_file_link = pdf_file.find('a')['href']
        pdf_link_tag = pdf_file.find('a')
        if not pdf_link_tag:
            print("No link found in this pdf file div.")
            return None

        pdf_file_url = pdf_link_tag['href']
        pdf_file_name_tag = pdf_file.find('p', class_='item-title')

        if pdf_file_name_tag:
            pdf_file_name = pdf_file_name_tag.text.strip()
            return {'name': pdf_file_name, 'url': pdf_file_url}

        return None

    def download_pdf(self, pdf_info):
        pdf_url = pdf_info['url']
        pdf_name = pdf_info['name']

        response = self.session.get(pdf_url, stream=True)
        response.raise_for_status()   # Ensure the request is successful
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', f"{pdf_name}.pdf")
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

        # Save PDF to media/pdfs
        with open(pdf_path, 'wb') as pdf_file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    pdf_file.write(chunk)

        # pdf_record = PDF(name=pdf_name)
        # with open(pdf_path, 'rb') as pdf_file:
        #     pdf_record.file_path.save(f"{pdf_name}.pdf", File(pdf_file), save=True)

        print(f"Downloaded and saved PDF: {pdf_name}")
        return pdf_path








