from django.contrib.auth import get_user_model
from rest_framework import serializers


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
                nickname=validated_data['nickname'],
                date_of_birth=validated_data['date_of_birth'],
                gender = validated_data['gender']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user
        else:
            raise Exception('Password do not match')
        
    
class GetUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields='__all__'

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','gender','date_of_birth','nickname')