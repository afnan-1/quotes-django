from django.contrib import admin
from django.urls import path,include
from .views import home,admin_import
urlpatterns = [
   path('admin-import/',admin_import,name='import'),
   path('',home,name='home'),
]