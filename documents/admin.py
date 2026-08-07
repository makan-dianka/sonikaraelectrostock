from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('document_type', 'company', 'reference', 'pdf', 'generated_by', 'is_deleted')

