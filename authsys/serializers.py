from rest_framework import serializers
from authsys.models import CustomUser

class UserSerializer(serializers.ModelSerializer):


    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }