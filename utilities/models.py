from django.db import models

# Create your models here.

# For PDF to image conversion
class PDFUpload(models.Model):
    pdf_file = models.FileField(upload_to='utilites/pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    zip_file = models.FileField(upload_to='utilites/zips/', null=True, blank=True)
    image_paths = models.JSONField(default=list)  # To store image file paths

    def __str__(self):
        return f"PDF uploaded at {self.uploaded_at}"