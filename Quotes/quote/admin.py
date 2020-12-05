from django.contrib import admin
from .models import Quote,AuthorAdmin

# Register your models here.
admin.site.register(Quote,AuthorAdmin)
admin.site.site_header = "The Quotes"
admin.site.index_title = "Quotes Adminstration"
admin.site.site_title = "Quotes Adminstration"

