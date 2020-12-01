from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Author,Quotes,Resource,AuthorAdmin
from django.contrib.auth.models import Group

class AccountAdmin(admin.ModelAdmin):
    search_fields=('first_name','last_name','sex','age','attribute')
    list_display=('first_name','last_name','age','sex','attribute')
    filter_horizontal=()
    list_filter=()
    fieldsets=()

admin.site.unregister(Group)
admin.site.register(Author,AccountAdmin)
admin.site.register(Quotes,AuthorAdmin)