import datetime as dt

from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models


class User(AbstractUser):
    ROLES = (('user', 'USER'), ('moderator', 'MODERATOR'), ('admin', 'ADMIN'))

    email = models.EmailField(max_length=254, unique=True, blank=False)
    first_name = models.CharField(max_length=150)
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    role = models.CharField(max_length=300, choices=ROLES, default=ROLES[0][0])

    def __str__(self):
        return f'{self.username}'


class ConfirmationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=4)


class Category(models.Model):
    """Категория произведения."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Уникальный фрагмент URL-адреса категории произведения',
        help_text=('Укажите уникальный фрагмент URL-адреса '
                   'для страницы группы. Используйте только латиницу, '
                   'цифры, дефисы и знаки подчёркивания'),
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанр произведения."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Уникальный фрагмент URL-адреса жанра произведения',
        help_text=('Укажите уникальный фрагмент URL-адреса '
                   'для жанра произведения. Используйте только латиницу, '
                   'цифры, дефисы и знаки подчёркивания'),
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведение."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения',
        help_text='Введите название произведения',
    )
    year = models.PositiveIntegerField(
        verbose_name='Год создания',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(dt.datetime.now().year)],
        help_text='Используйте формат года: YYYY')
    description = models.TextField(
        blank=True, null=True,
        verbose_name='Описание произведения',
        help_text='Добавление описания к произведению'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='Категория произведения',
        related_name='titles',
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """В этой модели будут связаны id жанра и id произведения."""
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, blank=True, null=True,)
    title = models.ForeignKey(
        Title, on_delete=models.SET_NULL, blank=True, null=True,)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    text = models.TextField(null=False, verbose_name='Отзыв')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1, 'Оценка не может быть ниже 1'),
            MaxValueValidator(10, 'Оценка не может быть больше 10')
        ],
        help_text='Поставьте оценку от 1 до 10',
        verbose_name='Оценка'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв {self.text} от {self.author} на {self.title}'


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    text = models.TextField(verbose_name='Комментарий')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий {self.text} от {self.author} к {self.review}'
        