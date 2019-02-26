from django.test import TestCase
from ..models import Movie, MovieComment


class TestMovieModel(TestCase):
    def setUp(self):
        Movie.objects.create(title='Karate Kids', year_of_production=1990)

    def test_movie__repr__(self):
        movie = Movie.objects.get(title='Karate Kids')
        self.assertEqual(movie.__repr__(), 'Karate Kids (1990)')

    def test_movie__str__(self):
        movie = Movie.objects.get(title='Karate Kids')
        self.assertEqual(movie.__repr__(), 'Karate Kids (1990)')


class TestMovieCommentModel(TestCase):
    def setUp(self):
        movie = Movie.objects.create(
            title='Karate Kids', year_of_production=1990)
        MovieComment.objects.create(movie=movie, comment_content='test')

    def test_comment__repr__(self):
        comment = MovieComment.objects.all().last()
        self.assertEqual(
            comment.__repr__(), 'MovieComment (Karate Kids): test')

    def test_comment__str__(self):
        comment = MovieComment.objects.all().last()
        self.assertEqual(
            comment.__str__(), 'MovieComment (Karate Kids): test')
