from django.db import models
from django.conf import settings


class Article(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Community_Article'
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    view = models.IntegerField(default=0)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, default=None, related_name='like_articles'
    )

class Comment(models.Model):
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_articles'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    