
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import *


router = SimpleRouter()
router.register('movie', MovieViewSet, 'movie')
router.register('genre', GenreViewSet, 'genre')
router.register('reviews', ReviewViewSet, 'reviews')


urlpatterns = [
    path('', include(router.urls)),
    path('favourite/', FavouriteView.as_view()),
]
