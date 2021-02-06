from django.contrib import admin
from .models import Quote,AuthorAdmin,QuoteOfDay

# Register your models here.
admin.site.register(QuoteOfDay)
admin.site.register(Quote,AuthorAdmin)
admin.site.site_header = "QOTRT"
admin.site.index_title = "QOTRT Adminstration"
admin.site.site_title = "Quotes Adminstration"

