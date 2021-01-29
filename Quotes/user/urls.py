from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('signup', SignUpApiViewSet,
                basename='SignupApi')
router.register('listusers',GetUserList, basename="ListUsers")
router.register('updateuser', UpdateUser,basename='updateusers')
urlpatterns = [
    path('', include(router.urls)),
    path('login/', UserLoginApiView.as_view()),
    # path('updateuser/<int:pk>/',UpdateUser.as_view()),
    path('deleteuser/<int:pk>/',DeleteUser.as_view()),
    path('getuser/', get_user),
    path('getuser2/',UserView.as_view()),
    path('facebooklogin/', UserFacebookLoginApiView.as_view()),
    path('googlelogin/', UserGoogleLoginApiView.as_view()),
    # path('add-coins/', addcoins.as_view({'post': 'add'})),
]
