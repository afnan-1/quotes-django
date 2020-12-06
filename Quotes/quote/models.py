from django.db import models
from django.contrib import admin
from author.models import Author

class Quote(models.Model):
    quote = models.TextField(max_length=1000)
    difficulty = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.quote[:20]

class Resource(models.Model):
    resource = models.CharField(max_length=50)
    quotes = models.ForeignKey(Quote,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.resource

class ResourceInline(admin.TabularInline):
    model = Resource

class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        ResourceInline
    ]
   
    search_fields=('quote','difficulty','author__first_name','author__last_name','author__attribute')
    list_display=('quotes','difficulty','author','created_at','updated_at')
    fieldsets=()
    def quotes(self, obj):
        if obj.quote:
            return f'{obj.quote[:30]}...'
        else:
            return 'Not Available'
    def author__attribute(self,obj):
        return obj.author.first_name
