import sys
import random 

from django.core.management.base import BaseCommand, CommandError

from movies.models import (
    Category, Actor, Genre, Movie, MovieShots, RatingStar,
    Rating, Review
)

class Command(BaseCommand):
    
    def handle(self, count=1000, *args, **options):
        desc = """fringilla ut morbi tincidunt augue interdum velit euismod 
            in pellentesque massa placerat duis ultricies lacus sed turpis tincidunt 
            id aliquet risus feugiat in ante metus dictum at tempor commodo ullamcorper 
            a lacus vestibulum sed arcu non odio euismod lacinia at quis risus sed 
            vulputate odio ut enim blandit volutpat maecenas volutpat blandit aliquam 
            etiam erat velit scelerisque in dictum non consectetur a erat nam at lectus 
            urna duis convallis convallis tellus id interdum velit laoreet id donec 
            ultrices tincidunt arcu
        """
    
        a = list((Category(name=f'Dummy category {i+1}', slug=f"dummycategory{i+1}", description=desc) for i in range(10)))
        Category.objects.bulk_create(a)
        print('done')


        b = list((Actor(name=f'Dummy Actor {i+1}', age=i+40, desc=desc) for i in range(10)))
        Actor.objects.bulk_create(b)
        print('done')


        c = list((Genre(name=f'Dummy genre {i+1}', slug=f"dummygenre{i+1}", description=desc) for i in range(10)))
        Genre.objects.bulk_create(c)
        print('done')
       
        cat = Category.objects.all().last()

        d = list((Movie(
            title=f'Dummy movie {i+1}', tagline=f'Dummy movie {i+1}', 
            description=desc, year=2023, country=f'Some country {i}', budget=8000*i,
            fees_in_usa=10000*i, fess_in_world=12000*i, category=cat,
            slug=f'dummymovie{i+1}') for i in range(100)))
        Movie.objects.bulk_create(d)

        print('done')