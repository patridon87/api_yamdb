import datetime as dt

from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Category, Genre, GenreTitle, Title, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')

    def valideate(data):
        if 'username' not in data:
            raise serializers.ValidationError('Поле username обязательное')

        if 'email' not in data:
            raise serializers.ValidationError('Поле email обязательное')

    def create():
        pass


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='name')

    class Meta:
        model = Category
        fields = ('category_name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    genre_name = serializers.CharField(source='name')

    class Meta:
        model = Genre
        fields = ('genre_name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genres = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'name', 'year', 'description', 'category',
            'genre', 'rating', )

    def get_rating(self, obj):
        if obj.reviews.exists():
            return round(obj.reviews.aggregate(
                rating=Avg('score')).get('rating'))
        return None


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genres = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'category', 'genre',)

    def create(self, validated_data):
        if 'genres' not in self.initial_data:
            title = Title.objects.create(**validated_data)
            return title
        else:
            genres = validated_data.pop('genres')
            title = Title.objects.create(**validated_data)
            for genre in genres:
                current_genre, status = Genre.objects.get_or_create(
                    **genre)
                GenreTitle.objects.create(
                    genre=current_genre, title=title)
            return title

    def validate_year(self, value):
        current_year = dt.datetime.now().year
        if 0 > value > current_year:
            raise serializers.ValidationError(
                'Год выпуска не может быть меньше 0 или больше текущего года!'
            )
        return value
