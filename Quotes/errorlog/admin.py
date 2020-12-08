from django.contrib import admin
from .models import ErrorMessage
# Register your models here.
class ErrorAdmin(admin.ModelAdmin):
    search_fields=('type_error',)
    list_display=('message','type_error','created_at','updated_at')
    # filter_horizontal=()
    # list_filter=()
    # fieldsets=()

admin.site.register(ErrorMessage, ErrorAdmin)