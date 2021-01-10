from django.urls import path, include
from .views import *
urlpatterns = [
    path('list/<int:pk>/',quote_list_of_author)

]