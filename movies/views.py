from rest_framework import (
    response,
    views,
    status
)

from .models import Movie
from .serializers import (
    MovieListSerializer, MovieRetrieveSerializer, ReviewCreateSerializer,
    CreateRatingSerializer
)


class MovieListAPIView(views.APIView):
    """Show list of movies"""

    def get(self, request):
        movies = Movie.objects.filter(draft=False)
        serializer = MovieListSerializer(movies, many=True)
        return response.Response(serializer.data)
    

class MovieRetrieveAPIView(views.APIView):
    """Show list of movies"""

    def get(self, request, pk):
        movie = Movie.objects.get(id=pk, draft=False)
        serializer = MovieRetrieveSerializer(movie)
        return response.Response(serializer.data)
    

class ReviewCreateAPIView(views.APIView):
    
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return response.Response(status=status.HTTP_201_CREATED)
    

class AddRatigStartAPIView(views.APIView):

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=self.get_client_ip(request))
            return response.Response(status=status.HTTP_201_CREATED)
        else:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)