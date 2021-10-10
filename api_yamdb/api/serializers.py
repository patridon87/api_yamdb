import datetime as dt

from django.db.models import Avg
from rest_framework import serializers

from reviews.models import (
    Category, Genre, GenreTitle,
    Title, User, Review, Comment
)


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError('Имя пользователя me запрещено')
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')

    def validate(self, data):
        request = self.context['request']
        method = request.method
        user = request.user
        if method == 'PATCH' and user.role == 'user' and 'role' in data:
            data.pop('role')
        return data


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genres = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        if obj.reviews.exists():
            return round(obj.reviews.aggregate(
                rating=Avg('score')).get('rating'))
        return None

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description',
            'genres', 'category', 'rating')


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genres = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'category', 'genres',)

    def validate_year(self, value):
        current_year = dt.datetime.now().year
        if 0 > value > current_year:
            raise serializers.ValidationError(
                'Год выпуска не может быть меньше 0 или больше текущего года!'
            )
        return value

    # def create(self, validated_data):
    #     if 'genres' not in self.initial_data:
    #         return Title.objects.create(**validated_data)
    #     else:
    #         genres = validated_data.pop('genres')
    #         title = Title.objects.create(**validated_data)
    #         for genre in genres:
    #             current_genre, status = Genre.objects.get_or_create(
    #                 **genre)
    #             GenreTitle.objects.create(
    #                 genre=current_genre, title=title)
    #         return title

    def create(self, validated_data):
        if 'genres' not in self.initial_data:
            raise serializers.ValidationError(
                'Поле жанр обязательно для заполнения!')
        else:
            genres = validated_data.pop('genres')
            for genre in genres:
                current_genre, status = Genre.objects.get_or_create(
                    **genre)
                genre.save()
                title = Title.objects.create(**validated_data)
                title.save()
                # title.genres.add(genre)
                # GenreTitle.objects.create(
                #     genre=current_genre, title=title)
            return title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data):
        user = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if self.context['request'].method != 'POST':
            return data
        if Review.objects.filter(title=title_id, author=user).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение'
            )
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)
