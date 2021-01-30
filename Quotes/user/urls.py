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
    path('deleteuser/<int:pk>/',DeleteUser.as_view()),
    path('getuser2/',UserView.as_view()),
    path('facebooklogin/', UserFacebookLoginApiView.as_view()),
    path('googlelogin/', UserGoogleLoginApiView.as_view()),
]
