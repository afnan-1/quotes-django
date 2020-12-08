from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Author
from django.contrib.auth.models import Group

class AccountAdmin(admin.ModelAdmin):
    search_fields=('first_name','last_name','sex','attribute')
    list_display=('first_name','last_name','num_of_quotes','sex','attribute','age')
    fields=('first_name','middle_name','last_name','sex','date_of_birth','date_of_death','attribute','photo','alias','bio')
    filter_horizontal=()
    list_filter=()
    fieldsets=()

admin.site.register(Author,AccountAdmin)