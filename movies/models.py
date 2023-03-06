from django.db import models
from datetime import date


class Category(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    slug = models.SlugField(max_length=160, unique=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Actor(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField(default=0)
    desc = models.TextField()
    image = models.ImageField(upload_to='actors/', blank=True, null=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Actors and Directors'
        verbose_name_plural = 'Actors and Directors'


class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(max_length=160, unique=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Movie(models.Model):
    title = models.CharField(max_length=100)
    tagline = models.CharField(max_length=100, default='')
    description = models.TextField()
    poster = models.ImageField(upload_to='movies/', blank=True, null=True)
    year = models.PositiveSmallIntegerField(default=2023)
    country = models.CharField(max_length=30)
    directors = models.ManyToManyField(Actor, related_name='film_director')
    actors = models.ManyToManyField(Actor, related_name='film_actor')
    genres = models.ManyToManyField(Genre)
    world_premiere = models.DateField(default=date.today)
    budget = models.PositiveIntegerField(default=0, help_text='Show in dollars')
    fees_in_usa = models.PositiveIntegerField(default=0, help_text='Show in dollars')
    fess_in_world = models.PositiveIntegerField(default=0, help_text='Show in dollars')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'


class MovieShots(models.Model):
    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=10)
    image = models.ImageField(upload_to='movie_shots/')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
    

class RatingStar(models.Model):
    value = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Rating's star"
        verbose_name_plural = "Rating's stars"
        ordering = ["-value"]


class Rating(models.Model):
    ip = models.CharField(max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')

    def __str__(self) -> str:
        return f"{self.star} -> {self.movie}"
    
    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'


class Review(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    text = models.TextField(max_length=5000)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True, related_name='childrens'
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self) -> str:
        return f"{self.name} -> {self.movie}"
    
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
    