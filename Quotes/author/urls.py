from django.contrib import admin
from django.urls import path,include
from .views import home,admin_import, authors_list
urlpatterns = [
   path('admin-import/',admin_import,name='import'),
   path('user/',include('user.urls')),
   path('author/list', authors_list ),
   path('',home,name='home'),
]