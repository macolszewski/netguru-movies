import requests
from net_movies import settings
from rest_framework import serializers
from .models import Movie, MovieComment


def get_movie(title):
    # Method that retrieves movie object from OMBD API data for given title

    response = requests.get(
        'http://www.omdbapi.com/',
        params={'t': title, 'apikey': settings.OMDB_API_KEY})

    if response.status_code == 200:
        data = response.json()

        return Movie.objects.get_or_create(
            title=data["Title"],
            year_of_production=data['Year'],
            omdb_data=data)[0]\
            if data.get('Title', None) else None


class MovieSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'year_of_production']


class MovieCommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = MovieComment
        fields = ['id', 'movie', 'comment_content']


def movie_as_dict(movie):
    return {
        'id': movie.id,
        'title': movie.title,
        'year_of_production': movie.year_of_production
    }


def comment_as_dict(comment):
    return {
        'id': comment.id,
        'movie': comment.movie.id,
        'comment_content': comment.comment_content
    }
