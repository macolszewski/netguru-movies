from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from net_movies.movies_api.utils import (
    MovieSerializer,
    MovieCommentSerializer,
    movie_as_dict
)
from net_movies.movies_api.models import Movie, MovieComment

MOVIES_ENDPOINT_URL = '/movies'
COMMENTS_ENDPOINT_URL = '/comments'
TOP_ENDPOINT_URL = '/top'

MOVIE_TITLES = ['Avatar', 'Karate Kids']
UNKNOWN_TITLE = 'randomtitle321'
REAL_YEAR = 1990

TEST_COMMENT_CONTENT = 'test-comment-content'

api = APIClient()


class TestOMDBAPI(TestCase):

    def test_empty_respone(self):
        response = api.get(MOVIES_ENDPOINT_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, [])

    def test_get_movie_after_posting_it(self):
        api.post(
            MOVIES_ENDPOINT_URL,
            data={'title': MOVIE_TITLES[0]},
            format='json'
        )

        response = api.get(MOVIES_ENDPOINT_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_count_movies_after_posting_several_times(self):
        for i in range(4):
            api.post(
                MOVIES_ENDPOINT_URL,
                data={'title': MOVIE_TITLES[i % 2]},
                format='json'
            )

        response = api.get(MOVIES_ENDPOINT_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Movie.objects.all().count(), 2)

    def test_get_movie_by_title(self):
        for i in range(2):
            api.post(
                MOVIES_ENDPOINT_URL,
                data={'title': MOVIE_TITLES[i]},
                format='json')

        response = api.get(
            MOVIES_ENDPOINT_URL, data={'title': MOVIE_TITLES[0]})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_movies_by_year(self):
        for i in range(2):
            api.post(
                MOVIES_ENDPOINT_URL,
                data={'title': MOVIE_TITLES[i]},
                format='json')

        response = api.get(
            MOVIES_ENDPOINT_URL, data={'year': REAL_YEAR})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_movie_by_year_and_title(self):
        for i in range(2):
            api.post(
                MOVIES_ENDPOINT_URL,
                data={'title': MOVIE_TITLES[i]},
                format='json')

        response = api.get(
            MOVIES_ENDPOINT_URL,
            data={'title': MOVIE_TITLES[1], 'year': REAL_YEAR})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_movie_by_unknown_title(self):
        for i in range(2):
            api.post(
                MOVIES_ENDPOINT_URL,
                data={'title': MOVIE_TITLES[i]},
                format='json')

        response = api.get(MOVIES_ENDPOINT_URL, data={'title': UNKNOWN_TITLE})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 0)

    def test_get_movies_by_bad_filter_ingoring_filters(self):
        for i in range(2):
            api.post(
                MOVIES_ENDPOINT_URL,
                data={'title': MOVIE_TITLES[i]},
                format='json')

        response = api.get(MOVIES_ENDPOINT_URL, data={'test': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 2)

    def test_post_movie(self):
        response = api.post(
            MOVIES_ENDPOINT_URL,
            data={'title': MOVIE_TITLES[0]},
            format='json')

        movie = Movie.objects.last()
        data = movie_as_dict(movie)
        serializer = MovieSerializer(data=data)

        self.assertEqual(movie.title, MOVIE_TITLES[0])
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_bad_request_when_posting_movie(self):
        response = api.post(
            MOVIES_ENDPOINT_URL,
            data={'test': 'test'},
            format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_posting_unknown_movie(self):
        response = api.post(
            MOVIES_ENDPOINT_URL,
            data={'title': UNKNOWN_TITLE},
            format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_movie(self):
        api.post(
            MOVIES_ENDPOINT_URL,
            data={'title': MOVIE_TITLES[0]},
            format='json')

        response = api.delete(
            MOVIES_ENDPOINT_URL,
            data={'title': MOVIE_TITLES[0]},
            format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Movie.objects.last())


class TestMovieCommentsAPI(TestCase):

    def test_empty_response(self):
        response = api.get(COMMENTS_ENDPOINT_URL)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, [])

    def test_posting_comment(self):
        api.post(
            MOVIES_ENDPOINT_URL,
            data={'title': MOVIE_TITLES[0]},
            format='json')

        response = api.post(
            COMMENTS_ENDPOINT_URL,
            data={
                'movie': Movie.objects.get(title=MOVIE_TITLES[0]).id,
                'comment_content': TEST_COMMENT_CONTENT})

        serializer = MovieCommentSerializer(data=response.data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(serializer.is_valid())

    def test_post_comment_to_unknown_movie(self):
        response = api.post(
            COMMENTS_ENDPOINT_URL,
            data={
                'movie': 9999999,
                'comment_content': TEST_COMMENT_CONTENT})

        serializer = MovieCommentSerializer(data=response.data)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(serializer.is_valid())

    def test_post_comment_without_content(self):
        api.post(
            MOVIES_ENDPOINT_URL,
            data={'title': MOVIE_TITLES[0]},
            format='json')

        response = api.post(
            COMMENTS_ENDPOINT_URL,
            data={
                'movie': Movie.objects.last().id,
                'comment_content': ''})

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_comments_by_blank_movie_id(self):
        for i in range(2):
            api.post(
                MOVIES_ENDPOINT_URL,
                data={'title': MOVIE_TITLES[i]},
                format='json')
            api.post(
                COMMENTS_ENDPOINT_URL,
                data={
                    'movie': Movie.objects.get(title=MOVIE_TITLES[i]).id,
                    'comment_content': TEST_COMMENT_CONTENT})

        response = api.get(COMMENTS_ENDPOINT_URL, data={'movie': ""})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_comments_by_movie_id(self):
        for i in range(2):
            api.post(
                MOVIES_ENDPOINT_URL,
                data={'title': MOVIE_TITLES[i]},
                format='json')
            api.post(
                COMMENTS_ENDPOINT_URL,
                data={
                    'movie': Movie.objects.get(title=MOVIE_TITLES[i]).id,
                    'comment_content': TEST_COMMENT_CONTENT})

        response = api.get(
            COMMENTS_ENDPOINT_URL,
            data={
                'movie': Movie.objects.get(title=MOVIE_TITLES[0]).id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_comments_by_unknown_movie_id(self):
        for i in range(2):
            api.post(
                MOVIES_ENDPOINT_URL,
                data={'title': MOVIE_TITLES[i]},
                format='json')
            api.post(
                COMMENTS_ENDPOINT_URL,
                data={
                    'movie': Movie.objects.get(title=MOVIE_TITLES[i]).id,
                    'comment_content': TEST_COMMENT_CONTENT})

        response = api.get(COMMENTS_ENDPOINT_URL, data={'movie': 999999})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_count_comments_after_posting(self):
        api.post(
            MOVIES_ENDPOINT_URL,
            data={'title': MOVIE_TITLES[0]}, format='json')

        for i in range(2):
            api.post(
                COMMENTS_ENDPOINT_URL,
                data={
                    'movie': MOVIE_TITLES[0],
                    'comment_content': TEST_COMMENT_CONTENT})

        response = api.get(COMMENTS_ENDPOINT_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_delete_comment(self):
        api.post(
            MOVIES_ENDPOINT_URL,
            data={'title': MOVIE_TITLES[0]},
            format='json')
        api.post(
            COMMENTS_ENDPOINT_URL,
            data={
                'movie': Movie.objects.get(title=MOVIE_TITLES[0]).id,
                'comment_content': TEST_COMMENT_CONTENT})

        response = api.delete(
            COMMENTS_ENDPOINT_URL,
            data={'id': MovieComment.objects.last().id},
            format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(MovieComment.objects.last())


class TestTopAPI(TestCase):
    def test_empty_response(self):
        response = api.get(TOP_ENDPOINT_URL)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, [])

    def test_get_top_movies_different_ranking(self):
        for i in range(2):
            api.post(
                MOVIES_ENDPOINT_URL,
                data={'title': MOVIE_TITLES[i]},
                format='json')
            api.post(
                COMMENTS_ENDPOINT_URL,
                data={
                    'movie': Movie.objects.get(
                        title=MOVIE_TITLES[i]).id,
                    'comment_content': TEST_COMMENT_CONTENT})

        api.post(
            COMMENTS_ENDPOINT_URL,
            data={
                'movie': Movie.objects.get(
                    title=MOVIE_TITLES[1]).id,
                'comment_content': TEST_COMMENT_CONTENT})

        response = api.get(TOP_ENDPOINT_URL)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 2)
        self.assertEquals(response.data[0]['rank'], 1)
        self.assertEquals(response.data[1]['rank'], 2)

    def test_get_top_movies_same_ranking(self):
        for i in range(2):
            api.post(
                MOVIES_ENDPOINT_URL,
                data={'title': MOVIE_TITLES[i]},
                format='json')
            api.post(
                COMMENTS_ENDPOINT_URL,
                data={
                    'movie': Movie.objects.get(
                        title=MOVIE_TITLES[i]).id,
                    'comment_content': TEST_COMMENT_CONTENT})

        response = api.get(TOP_ENDPOINT_URL)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 2)
        self.assertEquals(response.data[0]['rank'], 1)
        self.assertEquals(response.data[1]['rank'], 1)
