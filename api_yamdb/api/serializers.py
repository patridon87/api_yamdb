from rest_framework import serializers

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def valideate(data):
        if 'username' not in data:
            raise serializers.ValidationError('Поле username обязательное')
        
        if 'email' not in data:
            raise serializers.ValidationError('Поле email обязательное')

    def create():
        pass