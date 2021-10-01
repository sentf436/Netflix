from rest_framework import serializers
from movie.models import Movie, Genre, Favourite, Review


# from review.serializers import ReviewDetailSerializer


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'image', 'title', 'genre', 'link', 'avr_rating', 'created_at')


class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('genre', 'title', 'image', 'favourite', 'likes')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['reviews'] = ReviewDetailSerializer(instance.reviews.all(), many=True).data
        rep['likes'] = instance.likes.count()
        rep['favourite'] = instance.favourite.count()
        return rep


class MovieCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        exclude = ('user',)

    def create(self, validated_data):
        request = self.context.get('request')
        if request.user.is_anonymous:
            raise serializers.ValidationError('Добавлять могут только авторизованные пользователи')
        validated_data['user'] = request.user
        return super().create(validated_data)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class FavouriteMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'

        def get_favourite(self, obj):
            if obj.favourite:
                return obj.favourite
            return ''

        def to_representation(self, instance):
            rep = super().to_representation(instance)
            rep['favourite'] = self.get_favourite(instance)
            return rep


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
