from rest_framework import serializers

from reviews.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')



    def validate(self, data):

        if data['username'] == 'me':
            raise serializers.ValidationError('Имя пользователя me запрещено')
        return data

    # def create(self, validated_data):
    #     return User.objects.get_or_create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
