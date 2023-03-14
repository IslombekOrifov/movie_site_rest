from django.db.models import Q, Sum, Count, F

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import (
    generics,
)

from .models import Movie, Actor, Review
from .serializers import (
    MovieListSerializer, MovieRetrieveSerializer, 
    ReviewCreateSerializer, CreateRatingSerializer, 
    ActorListSerializer, ActorRetrieveSerializer
)
from .services import get_client_ip
from .filters import MovieFilter


class MovieListAPIView(generics.ListAPIView):
    """Show list of movies"""

    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=Count('ratings', filter=Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(middle_star=Sum(F('ratings__star')) / Count(F('ratings')))

        return movies
    

class MovieRetrieveAPIView(generics.RetrieveAPIView):
    """Show list of movies"""
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieRetrieveSerializer


class ReviewCreateAPIView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer
        

class AddRatigStartAPIView(generics.CreateAPIView):
    
    serializer_class = CreateRatingSerializer
    
    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))
    

class ActorListAPIView(generics.ListAPIView):


    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorRetrieveAPIView(generics.RetrieveAPIView):
    """Details for actor or director"""

    queryset = Actor.objects.all()
    serializer_class = ActorRetrieveSerializer