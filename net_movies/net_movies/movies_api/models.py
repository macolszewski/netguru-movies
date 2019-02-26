from django.db import models
from jsonfield import JSONField


class Movie(models.Model):
    title = models.CharField(max_length=255)
    year_of_production = models.IntegerField()
    omdb_data = JSONField()

    def __str__(self):
        return '{0} ({1})'.format(self.title, self.year_of_production)

    def __repr__(self):
        return '{0} ({1})'.format(self.title, self.year_of_production)


class MovieComment(models.Model):
    comment_content = models.TextField()
    movie = models.ForeignKey(
        Movie, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return 'MovieComment ({0}): {1}'\
            .format(self.movie.title, self.comment_content)

    def __repr__(self):
        return 'MovieComment ({0}): {1}'\
            .format(self.movie.title, self.comment_content)
