from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
# router.register('list', listDataSet,basename='listdataset')
# router.register('update/', updateDataSet, basename='update')
urlpatterns = [
    path('', include(router.urls)),
    path('authorslist/<int:pk>/', dataset_detail),
    path('list/', list_dataset),
    path('discussionmode/<int:pk>/', discussion_mode),
    path('delete/<int:pk>/',delete_dataset),
    path('create/',createDataSet),
    path('update/<int:pk>',updateDataSet)
]