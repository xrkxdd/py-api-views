
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, mixins, viewsets, status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from cinema.models import Movie, Genre, Actor, CinemaHall
from cinema.serializers import (
    MovieSerializer,
    GenreSerializer,
    ActorSerializer,
    CinemaHallSerializer
)


class GenreList(APIView):
    @staticmethod
    def get(request) -> Response:
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request) -> Response:
        serializer = GenreSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GenreDetail(APIView):
    @staticmethod
    def get_object(pk: int) -> Genre:
        return get_object_or_404(Genre, pk=pk)

    def get(self, request, pk: int) -> Response:
        serializer = GenreSerializer(self.get_object(pk=pk))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk: int) -> Response:
        instance = self.get_object(pk=pk)
        serializer = GenreSerializer(instance, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk: int) -> Response:
        self.get_object(pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk: int) -> Response:
        serializer = GenreSerializer(
            self.get_object(pk=pk),
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ActorList(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def get(self, request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs) -> Response:
        return self.create(request, *args, **kwargs)


class ActorDetail(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def get(self, request, *args, **kwargs) -> Response:
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs) -> Response:
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs) -> Response:
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs) -> Response:
        return self.destroy(request, *args, **kwargs)


class CinemaHallViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
