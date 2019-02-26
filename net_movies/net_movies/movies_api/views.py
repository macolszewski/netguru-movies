from django.shortcuts import get_object_or_404
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
        title = request.POST.get('title', None)

        if title:
            movie = get_movie(title)

            if movie:
                serializer = MovieSerializer(data=movie_as_dict(movie))

                if serializer.is_valid():
                    return Response(
                        serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors if movie else "Movie not found",
            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        title = request.POST.get('title', None)
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
        serializer = MovieCommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        comment_id = request.POST.get('id', None)

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
