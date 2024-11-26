from django.db import models
from django.conf import settings


class Ending(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Ending',)
    movie_id = models.ForeignKey("Movie", related_name='Movie', on_delete=models.CASCADE)
    prompt = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    view = models.IntegerField(default=0)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, default=None, related_name='like_endings'
    )
    dislike_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, default=None, related_name='dislike_endings'
    )



class Movie(models.Model):
    title = models.CharField(max_length=100)
    openYear = models.IntegerField()
    synopsis = models.TextField()
    plot = models.TextField()
    is_selected = models.BooleanField(default=True)
    poster = models.ImageField(upload_to='movies', height_field=None, width_field=None, max_length=None, blank=True)


class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
    ending_id= models.ForeignKey("Ending", on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_endings')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
