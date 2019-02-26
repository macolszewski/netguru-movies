from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Movie
from .utils import (
    MovieSerializer,
    get_movie,
    movie_as_dict,
)


class Movies(APIView):
    def get(self, request, format=None):
        return Response(MovieSerializer(Movie.objects.all(), many=True).data)

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
