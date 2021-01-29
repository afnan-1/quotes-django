from django.shortcuts import render
from django.contrib.auth import get_user_model
from user.models import *
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from user.serializers import *
from django.db.models import Q
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
User = get_user_model()


# Create your views here.
class SignUpApiViewSet(viewsets.ModelViewSet):
    """Handle Registering new users"""
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        try:
            if request.data.get("email") and User.objects.filter(email=request.data.get("email")):
                return Response({
                    "status": "failure",
                    "message": "Email already exist",
                    "data": ""})

            elif request.data.get("username") and User.objects.filter(username=request.data.get("username")):
                return Response({
                    "status": "failure",
                    "message": "Username already exist",
                    "data": ""})
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({
                "status": "failure",
                "message": "User has not created - " + str(e),
                "data": ""
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""

    def post(self, request, *args, **kwargs):
        try:
            # import pdb; pdb.set_trace()
            request.data['username'] = request.data.get('email')
            queryset = User.objects.filter(
                Q(username=request.data.get("email")) | Q(email=request.data.get("email")))
            if len(queryset):
                if not queryset[0].check_password(request.data.get("password")):
                    return Response({
                        "status": "Failure",
                        "message": "Password",
                        "data": ""}, 
                                    status=status.HTTP_401_UNAUTHORIZED)
                if queryset[0].is_active == False:
                    return Response({
                        "status": "Failure",
                        "message": "User is Deactivated",
                        "data": ""}, 
                                    status=status.HTTP_401_UNAUTHORIZED)

                response = super().post(request, *args, **kwargs)
                token = Token.objects.get(key=response.data['token'])
                queryset = User.objects.get(id=token.user_id)
                serializer = GetUserListSerializer(queryset, many=False, context={'request':request})
                return Response({
                    "status": "success", 
                    "messege ": "User Log in", 
                    "data": {'token': token.key,'data':serializer.data},
                    'error':'false'
                    })
            return Response({
                "status": "Failure",
                "message": "Email",
                "data":""
                             },
                                status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                "status": "Failure",
                "message": "Login failed - " + str(e) ,
                "data":""},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserFacebookLoginApiView(ObtainAuthToken):
    """Handle login and signup for facebook """

    def post(self, request, *args, **kwargs):
        try:
            queryset = User.objects.filter(
                Q(email=request.data.get("email")))
            print(queryset)
            if len(queryset):
                if queryset[0].facebook_token != request.data.get("facebook_token"):
                    return Response({
                        "status":"failure",
                        "message": "Invalid Token",
                        "data":""}, 
                                    status=status.HTTP_401_UNAUTHORIZED)

                token, created = Token.objects.get_or_create(user=queryset[0])
                queryset = User.objects.get(id=token.user_id)
                return Response({
                    "status": "success",
                    "message": "User login successfully",
                    "data": {"token":token.key,'id':queryset.id, 'email': queryset.email, 'username': queryset.username,
                                 'name': queryset.name, 'gender': queryset.gender}
                    })

            else:
                firstname = request.data.get('first_name')
                lastname = request.data.get('last_name')
                name = firstname + ' ' + lastname

                user = User.objects.create(
                    first_name=firstname,
                    last_name=lastname,
                    name=name,
                    username=request.data.get('email'),
                    email=request.data.get('email'),
                    facebook_token=request.data.get('facebook_token'),
                )

                user.save()

                token, created = Token.objects.get_or_create(user=user)
                queryset = User.objects.get(id=token.user_id)

                return Response({
                    "status": "success",
                    "message": "user signup successfully", 
                    "data":{'token': token.key, 'email': queryset.email, 'username': queryset.username,
                    'name': queryset.name,  'gender': queryset.gender}
                    })

        except Exception as e:
            return Response({
                "status": "Failure",
                "message": "Login failed - " + str(e),
                "data":""}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserGoogleLoginApiView(ObtainAuthToken):
    """Handle login and signup for Google"""

    def post(self, request, *args, **kwargs):
        try:
            queryset = User.objects.filter(
                Q(email=request.data.get("email")))
            if len(queryset):
                if queryset[0].google_token != request.data.get("google_token"):
                    print(queryset[0].google_token)
                    return Response({
                        "status":"failure",
                        "message": "Invalid Token",
                        "data":""}, 
                                    status=status.HTTP_401_UNAUTHORIZED)

                token, created = Token.objects.get_or_create(user=queryset[0])
                queryset = User.objects.get(id=token.user_id)
                serializer = GetUserListSerializer(queryset,many=False, context={'request':request})
                return Response({
                    "status": "success",
                    "message": "User login successfully",
                    "data": {"token":token.key,'data':serializer.data}
                    })

            else:
                firstname = request.data.get('first_name')
                lastname = request.data.get('last_name')
                name = firstname + ' ' + lastname

                user = User.objects.create(
                    first_name=firstname,
                    last_name=lastname,
                    name=name,
                    username=request.data.get('email'),
                    email=request.data.get('email'),
                    google_token=request.data.get('google_token'),
                )

                user.save()

                token, created = Token.objects.get_or_create(user=user)
                queryset = User.objects.get(id=token.user_id)

                return Response({
                    "status": "success",
                    "message": "user signup successfully", 
                    "data":{'token': token.key, 'email': queryset.email, 'username': queryset.username,
                    'name': queryset.name,'first_name':queryset.first_name,'last_name':queryset.last_name,  'gender': queryset.gender,'id':queryset.id}
                    })

        except Exception as e:
            return Response({
                "status": "Failure",
                "message": "Login failed - " + str(e),
                "data":""}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            

class GetUserList(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = GetUserListSerializer
    permission_classes = (IsAuthenticated,)

# class UpdateUser(generics.RetrieveUpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UpdateUserSerializer
#     permission_classes = (AllowAny,)

class UpdateUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer

    def put(self,request,*args,**kwargs):
        pk = request.data.get('id')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        nickname = request.data.get('nickname')
        profile_picture = request.data.get('profile_picture')
        print(profile_picture)
        email = request.data.get('email')
        date_of_birth = request.data.get('date_of_birth')
        gender = request.data.get('gender')
        user = User.objects.get(pk=request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.nickname = nickname
        user.email = email
        user.date_of_birth = date_of_birth
        user.gender = gender
        user.profile_picture = profile_picture
        user.save()
        serializer = UpdateUserSerializer(user, many=False,context={"request":request} )
        return Response({'message':'updated user','data':serializer.data})

class DeleteUser(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = GetUserListSerializer
    # permission_classes = (IsAuthenticated,)


@api_view(['GET',])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = User.objects.get(pk=request.user.id)
    serializer = GetUserListSerializer(user, many=False)
    return Response({
        'message':"User Get Succesfully",
        'data':serializer.data,
        'success':True
    })
class UserView(APIView):

    def get(self, request, *args, **kwargs):

        queryset = User.objects.get(pk=request.user.id)
        serializer = GetUserListSerializer(queryset, many=False, context={"request":request})
        return Response(serializer.data)