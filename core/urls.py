from django.urls import path
from .views import PDFDownloadView

urlpatterns = [
    path('download-pdf/<str:pdf_name>/', PDFDownloadView.as_view(), name='download_pdf'),
]