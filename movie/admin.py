from django.contrib import admin
from .models import Movie, Genre, Favourite, Review


admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Favourite)
admin.site.register(Review)

