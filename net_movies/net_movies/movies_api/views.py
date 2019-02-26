from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Movie, MovieComment
from .utils import (
    MovieSerializer,
    MovieCommentSerializer,
    get_movie,
    movie_as_dict,
    comment_as_dict,
)


def home(request):
    return HttpResponse(
        '''
        <h1>Welcome</h1>
        To use app check instructions on
         <a href="https://github.com/macolszewski/netguru-movies">github</a>
        <h2>Available urls:</h2>
        <ul>
        <li><a href="/movies">movies</a></li>
        <li><a href="/comments">movies comments</a></li>
        <li><a href="/top">movies ranking</a></li>
        </ul
        '''
    )


class Movies(APIView):
    def get(self, request, format=None):
        movies = Movie.objects.all()
        year_of_production = request.GET.get('year', None)
        title_part = request.GET.get('title', None)

        if year_of_production:
            movies = movies.filter(year_of_production=year_of_production)\
                if year_of_production.isdigit() else movies

        if title_part:
            movies = movies.filter(title__contains=title_part)

        return Response(MovieSerializer(movies, many=True).data)

    def post(self, request, format=None):
        title = request.data.get('title', None)

        movie = get_movie(title) if title else None

        if movie:
            serializer = MovieSerializer(data=movie_as_dict(movie))

            if serializer.is_valid():
                return Response(
                    movie.omdb_data, status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors if movie else "Movie not found",
            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        title = request.data.get('title', None)
        if title:
            movie = get_object_or_404(
                Movie, title=title)
            serializer = MovieSerializer(data=movie_as_dict(movie))

            if serializer.is_valid():
                movie.delete()
                return Response(
                    serializer.data, status=status.HTTP_200_OK)

        return Response(
            serializer.errors if title else "Movie not found",
            status=status.HTTP_400_BAD_REQUEST)


class Comments(APIView):
    def get(self, request, format=None):
        comments = MovieComment.objects.all()
        movie_id = request.GET.get('movie', None)

        if movie_id:
            comments = comments.filter(movie=int(movie_id))\
                if movie_id.isdigit() else comments.filter(
                    movie=get_object_or_404(Movie, title=movie_id).id)

        serializer = MovieCommentSerializer(comments, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        movie_id = request.data.get('movie', None)

        if movie_id:
            movie_id = movie_id if movie_id.isdigit()\
                else get_object_or_404(Movie, title=movie_id).id
            data = {
                'movie': movie_id,
                'comment_content': request.data.get(
                    'comment_content', None)
            }
        serializer = MovieCommentSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        comment_id = request.data.get('id', None)

        if comment_id:
            comment = get_object_or_404(
                MovieComment, id=int(comment_id))

            serializer = MovieCommentSerializer(data=comment_as_dict(comment))

            if serializer.is_valid():
                comment.delete()
                return Response(
                    serializer.data, status=status.HTTP_200_OK)

        return Response(
            serializer.errors if comment_id else "Comment not found",
            status=status.HTTP_400_BAD_REQUEST)


class Top(APIView):
    def get(self, request, format=None):
        response_data = []
        movies = Movie.objects.all().annotate(Count('comments'))

        if movies:
            ranks = enumerate(
                list(set([m.comments__count for m in movies]))[::-1], 1)

            for rank, comments_count in ranks:
                for movie in movies.filter(comments__count=comments_count):
                    response_data.append({
                        'movie_id': movie.id,
                        'total_comments': comments_count,
                        'rank': rank})

        return Response(response_data)
