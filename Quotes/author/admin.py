from django.contrib import admin
from .models import Author,Attribute
from django.contrib.auth.models import Group

class AccountAdmin(admin.ModelAdmin):
    search_fields=('first_name','last_name','sex','attribute')
    list_display=('first_name','last_name','num_of_quotes','sex','age')
    fields=('first_name','middle_name','last_name','sex','date_of_birth','date_of_death','attribute','photo','alias','bio','age','num_of_quotes')
    filter_horizontal=('attribute',)
    list_filter=()
    fieldsets=()
    readonly_fields=('age','num_of_quotes')
admin.site.register(Attribute)
admin.site.register(Author,AccountAdmin)