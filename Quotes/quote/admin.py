from django.contrib import admin
from .models import Quotes,AuthorAdmin

# Register your models here.
admin.site.register(Quotes,AuthorAdmin)