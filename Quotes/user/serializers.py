from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from user.tokens import account_activation_token
from django.contrib.sites.models import Site

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    """Serializer for creating user"""
    # confirm_password = serializers.CharField(
    #     style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        # fields = ('username', 'email', 'name', 'password', 'confirm_password')
        fields=('email','password','nickname','date_of_birth','gender','first_name','last_name')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Function to create user"""
        if validated_data['password']:
            user = User.objects.create(
                username=validated_data['email'],
                email=validated_data['email'],
                first_name = validated_data['first_name'],
                last_name=validated_data['last_name'],
                nickname=validated_data['nickname'],
                date_of_birth=validated_data['date_of_birth'],
                gender = validated_data['gender']
            )
            user.set_password(validated_data['password'])
            user.is_active = False
            user.save()
            current_site = Site.objects.get_current()
            subject = 'Activate Your MySite Account'
            message = render_to_string('email_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return user
        else:
            raise Exception('Password do not match')
        
 
class GetUserListSerializer(serializers.HyperlinkedModelSerializer):
    profile_picture = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=True, required=False)
    class Meta:
        model = User
        fields = ('id','first_name','last_name','nickname','profile_picture','email','date_of_birth','gender')

class UpdateUserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=True, required=False)
    class Meta:
        model = User
        fields = ('id','first_name','last_name','nickname','profile_picture','email','date_of_birth','gender')
