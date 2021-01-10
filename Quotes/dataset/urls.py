from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
# router.register('list', listDataSet,basename='listdataset')
# router.register('update/', updateDataSet, basename='update')
urlpatterns = [
    path('', include(router.urls)),
    path('authorslist/', dataset_authorlist),
    path('list/', list_dataset),
    path('questions/<int:pk>/', get_questions),
    # path('delete/<int:pk>',DeleteDataSet.as_view()),
    path('create/',createDataSet),
    path('update/<int:pk>',updateDataSet)
]