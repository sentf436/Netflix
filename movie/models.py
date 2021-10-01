from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Genre(models.Model):
    genre = models.CharField("Жанр", max_length=75)
    slug = models.SlugField(primary_key=True)


class Movie(models.Model):
    genre = models.ForeignKey(Genre,
                              on_delete=models.CASCADE,
                              verbose_name="Жанр")
    title = models.CharField('Название', max_length=50)
    description = models.TextField('Описание')
    authors = models.CharField('Авторы', max_length=150)
    image = models.ImageField('Изображение')
    link = models.URLField('Видео')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='movie',
                             verbose_name="Автор",
                             default=User)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
        return self.likes.count()

    def total_favourites(self):
        return self.favourite.count()

    def avr_rating(self):
        summ = 0
        ratings = Review.objects.filter(movie=self)
        for rating in ratings:
            summ += rating.rate
        if len(ratings) > 0:
            return summ / len(ratings)
        else:
            return 'Нет рейтинга'


class Likes(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='likes')
    likes = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')


class Favourite(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='favourite')
    favourite = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


RATING_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='movie', related_name='reviews')
    text = models.TextField('Отзыв')
    rate = models.IntegerField('Оценка', choices=RATING_CHOICES)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
        unique_together = (('user', 'movie'),)
        index_together = (('user', 'movie'),)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.movie} --> {self.user}'
