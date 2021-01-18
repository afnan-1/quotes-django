from django.contrib import admin
from django.urls import path,include
from .views import home,admin_import, authors_detail, authors_list
urlpatterns = [
   path('admin-import/',admin_import,name='import'),
   path('user/',include('user.urls')),
   path('author/<int:pk>/', authors_detail ),
   path('author/list',authors_list),
   path('',home,name='home'),
]