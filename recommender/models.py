from django.db import models
from django.contrib.auth.models import Permission, User

class MovieInfo(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    movie_name = models.CharField(max_length=200)
    movie_rating = models.CharField(max_length=20)
    movie_plot = models.CharField(max_length=10000)
    movie_earn = models.CharField(max_length=20)
    movie_poster = models.CharField(max_length=1000)
    movie_year = models.CharField(max_length=10)
    movie_director = models.CharField(max_length=1000)
    movie_runtime = models.CharField(max_length=15)
    movie_stars = models.CharField(max_length=1500)
    star1 = models.BooleanField(default=False)
    star2 = models.BooleanField(default=False)
    star3 = models.BooleanField(default=False)
    star4 = models.BooleanField(default=False)
    star5 = models.BooleanField(default=False)
    user_rating = models.IntegerField(default=0)
    imdb = models.IntegerField(default=0)
    awards = models.CharField(max_length=1500)
    def __str__(self):
        return self.movie_name



# Create your models here.
