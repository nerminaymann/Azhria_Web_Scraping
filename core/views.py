from django.views import View
from django.http import JsonResponse, Http404
from .services.pdf_parser import PDFParser
from .models import PDF

class PDFDownloadView(View):
    base_url = "https://archive.org/details/azhria"

    def get(self, request, pdf_name):
        parser = PDFParser(self.base_url, pdf_name)
        pdf_files = parser.parse_pdf_files()

        if not pdf_files:
            raise Http404("No PDF files found for the specified name.")

        saved_pdfs = []
        for pdf_info in pdf_files:
            parser.download_pdf(pdf_info)

            pdf_record, created = PDF.objects.get_or_create(
                name=pdf_info['name'],
                defaults={'file_path': f"pdfs/{pdf_info['name']}.pdf"}
            )
            saved_pdfs.append({
                "name": pdf_record.name,
                "file_path": pdf_record.file_path.url,
                "downloaded_at": pdf_record.downloaded_at
            })

        return JsonResponse({"saved_pdfs": saved_pdfs})
