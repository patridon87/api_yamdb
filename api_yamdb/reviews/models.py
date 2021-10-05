import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

CATEGORIES = (
    ('Books', 'Книги'),
    ('Movies', 'Фильмы'),
    ('Music', 'Музыка'),
)

TITLE_CHOICES = [
    ('Books', (
        ('Fiction', 'Фантастика'),
        ('Classic', 'Классика'),
        ('Detective', 'Детектив'),)),
    ('Music', (
        ('Rock-n-Roll', 'Рок-н-Ролл'),
        ('Classic', 'Классика'),
        ('Blues', 'Блюз'),)),
    ('Movies', (
        ('Drama', 'Драма'),
        ('Comedy', 'Комедия'),
        ('Detective', 'Детектив'),)),
]


class Category(models.Model):
    """Категория произведения."""
    name = models.CharField(max_length=256, choices=CATEGORIES)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Уникальный фрагмент URL-адреса категории произведения',
        help_text=('Укажите уникальный фрагмент URL-адреса '
                   'для страницы группы. Используйте только латиницу, '
                   'цифры, дефисы и знаки подчёркивания'),
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Genre(models.Model):
    """Жанр произведения."""
    name = models.CharField(max_length=256, choices=TITLE_CHOICES)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Уникальный фрагмент URL-адреса жанра произведения',
        help_text=('Укажите уникальный фрагмент URL-адреса '
                   'для жанра произведения. Используйте только латиницу, '
                   'цифры, дефисы и знаки подчёркивания'),
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения',
        help_text='Введите название произведения',
    )
    year = models.PositiveIntegerField(
        verbose_name='Год создания',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(datetime.now().year)],
        help_text="Используйте формат года: YYYY")
    rating = models.PositiveIntegerField(default=None, blank=True, null=True)
    description = models.TextField(
        blank=True,
        verbose_name='Описание произведения',
        help_text='Добавление описания к произведению'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория произведения',
        related_name='titles',
    )
    genre = models.ManyToManyField(
        Genre,
        on_delete=models.SET_NULL,
        verbose_name='Жанр произведения',
        related_name='titles',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
