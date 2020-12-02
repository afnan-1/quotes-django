from django.db import models
from django.contrib import admin
from author.models import Author

class Quotes(models.Model):
    quote = models.TextField(max_length=1000)
    difficulty = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.quote[:20]

class Resource(models.Model):
    resource = models.CharField(max_length=50)
    quotes = models.ForeignKey(Quotes,on_delete=models.CASCADE)
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
    list_display=('quote','difficulty','author','created_at','updated_at')
    def quote(self, obj):
        if obj.quote:
            return f'{obj.quote[:30]}...'
        else:
            return 'Not Available'