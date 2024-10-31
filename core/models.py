from django.db import models

class PDF(models.Model):
    name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='pdfs/')
    downloaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
