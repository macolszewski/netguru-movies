from django.test import TestCase
from net_movies.movies_api.utils import (
    MovieSerializer,
    MovieCommentSerializer,
    movie_as_dict,
    comment_as_dict,
    get_movie
)
from net_movies.movies_api.models import Movie, MovieComment
from .test_api import (
    MOVIE_TITLES,
    UNKNOWN_TITLE,
    COMMENTS_ENDPOINT_URL,
    TEST_COMMENT_CONTENT
)
from rest_framework.test import APIClient

api = APIClient()


class TestUtils(TestCase):
    def test_getting_movie_correct_title(self):
        movie = get_movie(MOVIE_TITLES[0])
        self.assertEqual(movie, Movie.objects.last())

    def test_getting_movie_unknown_title(self):
        self.assertFalse(get_movie(UNKNOWN_TITLE))

    def test_movie_serializer_correct_movie(self):
        movie = get_movie(MOVIE_TITLES[0])
        serializer = MovieSerializer(data=movie_as_dict(movie))
        self.assertTrue(serializer.is_valid())
        self.assertEqual(
            serializer.data,
            {'title': 'Avatar', 'year_of_production': 2009})

    def test_movie_serializer_unknown_movie(self):
        movie = get_movie(UNKNOWN_TITLE)
        serializer = MovieSerializer(data=movie_as_dict(movie))
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.data, {})

    def test_comment_serializer_correct_comment(self):
        movie = get_movie(MOVIE_TITLES[0])
        api.post(
            COMMENTS_ENDPOINT_URL,
            data={
                'movie': movie.id,
                'comment_content': TEST_COMMENT_CONTENT})
        comment = MovieComment.objects.last()
        serializer = MovieCommentSerializer(data=comment_as_dict(comment))
        self.assertTrue(serializer.is_valid())
        self.assertEqual(
            serializer.data,
            {'movie': movie.id, 'comment_content': TEST_COMMENT_CONTENT})

    def test_comment_serializer_unknown_comment(self):
        comment = MovieComment.objects.last()
        serializer = MovieCommentSerializer(data=comment_as_dict(comment))
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.data, {})

    def test_movie_as_dict_correct_movie(self):
        movie = get_movie(MOVIE_TITLES[0])
        self.assertEqual(
            movie_as_dict(movie),
            {
                'id': movie.id,
                'title': movie.title,
                'year_of_production': movie.year_of_production
            })

    def test_movie_as_dict_unknown_movie(self):
        movie = get_movie(UNKNOWN_TITLE)
        self.assertFalse(movie_as_dict(movie))

    def test_comment_as_dict_correct_comment(self):
        movie = get_movie(MOVIE_TITLES[0])
        api.post(
            COMMENTS_ENDPOINT_URL,
            data={
                'movie': movie.id,
                'comment_content': TEST_COMMENT_CONTENT})
        comment = MovieComment.objects.last()
        self.assertEqual(
            comment_as_dict(comment),
            {
                'id': comment.id,
                'movie': movie.id,
                'comment_content': TEST_COMMENT_CONTENT
            })

    def test_comment_as_dict_unknown_comment(self):
        comment = MovieComment.objects.last()
        self.assertFalse(comment_as_dict(comment))
