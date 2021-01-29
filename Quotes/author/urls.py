from django.contrib import admin
from django.urls import path,include
from .views import home,admin_import, authors_list,AuthorDetails
from rest_framework import routers
router = routers.DefaultRouter()
# router.register('author', AuthorDetails, basename='authors')

urlpatterns = [
   path('admin-import/',admin_import,name='import'),
   path('user/',include('user.urls')),
   path('', include(router.urls)),

   path('author/<int:pk>/', AuthorDetails.as_view() ),
   path('author/list',authors_list),
   path('',home,name='home'),
]