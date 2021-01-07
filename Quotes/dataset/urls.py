from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('', listDataSet,basename='listdataset')
# router.register('create', CreateDataSet,basename='createdataset')
urlpatterns = [
    # path('', include(router.urls)),
    # path('delete/<int:pk>',DeleteDataSet.as_view()),
    path('create/',createDataSet)
]