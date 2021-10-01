import django_filters
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filter, status

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import action

from movie.models import Movie, Genre, User, Likes, Favourite, Review
from movie.permissions import (IsAuthorOrIsAdmin, IsAuthor, IsAdminUser)
from movie.serializers import (MovieListSerializer, GenreSerializer,
                               MovieDetailSerializer, FavouriteMovieSerializer, MovieCreateSerializer,
                               ReviewListSerializer)


class MovieFilter(filters.FilterSet):
    created_at = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Movie
        fields = ('title', 'description', 'created_at', 'genre')


class GenreFilter(filters.FilterSet):
    created_at = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Genre
        fields = ('genre', 'created_at')


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer
    filter_backends = [filters.DjangoFilterBackend,
                       rest_filter.SearchFilter,
                       rest_filter.OrderingFilter]
    filterset_class = MovieFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == 'retrieve':
            return MovieDetailSerializer
        return MovieCreateSerializer

    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        movie = self.get_object()
        user = request.user
        try:
            like = Likes.objects.get(movie=movie, user=user)
            like.likes = not like.likes
            if like.likes:
                like.save()
            else:
                like.delete()
            message = 'нравится' if like.likes else 'не нравится'
        except Likes.DoesNotExist:
            Likes.objects.create(movie=movie, user=user, likes=True)
            message = 'нравится'
        return Response(message, status=200)

    @action(['POST'], detail=True)
    def favourite(self, request, pk=None):
        movie = self.get_object()
        user = request.user
        try:
            favourite = Favourite.objects.get(movie=movie, user=user)
            favourite.favourite = not favourite.favourite
            if favourite.favourite:
                favourite.save()
            else:
                favourite.delete()
            message = 'в избранном' if favourite.favourite else 'не в избранном'
        except Favourite.DoesNotExist:
            Favourite.objects.create(movie=movie, user=user, favourite=True)
            message = 'в избранном'
        return Response(message, status=200)

    def get_permission(self):

        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action == 'list':
            return []
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthor()]
        elif self.action in ['like', 'favourite']:
            return [IsAuthenticated()]
        else:
            return []


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend,
                       rest_filter.SearchFilter,
                       rest_filter.OrderingFilter]
    filterset_class = GenreFilter
    search_fields = ['name']
    ordering_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return GenreSerializer
        elif self.action == 'retrieve':
            return GenreSerializer
        return GenreSerializer


class FavouriteView(ListAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteMovieSerializer


class FavouritesListView(ListAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteMovieSerializer
    permission_classes = [IsAuthenticated, IsAuthor]


class ReviewFilter(filters.FilterSet):
    django_filters.CharFilter()

    class Meta:
        model = Review
        fields = ('user', 'movie', 'text')


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
    permission_classes = [IsAuthorOrIsAdmin, IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend,
                       rest_filter.SearchFilter,
                       rest_filter.OrderingFilter]

    filterset_class = ReviewFilter
    search_fields = ['text']
    ordering_fields = ['author', 'movie']

    def get_serializer_class(self):
        if self.action == 'list':
            return ReviewListSerializer
        elif self.action == 'retrieve':
            return ReviewListSerializer
        return ReviewListSerializer
