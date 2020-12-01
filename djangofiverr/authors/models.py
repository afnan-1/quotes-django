from django.db import models
from django.contrib import admin

# Create your models here.

class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    alias = models.CharField(max_length=1000)
    photo = models.ImageField(upload_to='images/')
    age = models.IntegerField()
    date_of_birth = models.DateField()
    SEX_CHOICES = (
        ('F', 'Female',),
        ('M', 'Male',),
    )
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
    )
    ATTRIBUTE_CHOICES = (
        ('Author','Author'),
        ('Athlete','Athlete'),
        ('Politician','Politician')
    )
    attribute = models.CharField(max_length=10,choices=ATTRIBUTE_CHOICES)
    bio = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + " "+ self.last_name





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
