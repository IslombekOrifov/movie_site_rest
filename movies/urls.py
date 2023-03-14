from django.urls import path

from . import views


urlpatterns = [
    path('movie/', views.MovieListAPIView.as_view()),
    path('movie/<int:pk>/', views.MovieRetrieveAPIView.as_view()),
    path('review/', views.ReviewCreateAPIView.as_view()),
    path('rating/', views.AddRatigStartAPIView.as_view()),
    path('actors/', views.ActorListAPIView.as_view()),
    path('actors/<int:pk>/', views.ActorRetrieveAPIView.as_view()),
]
