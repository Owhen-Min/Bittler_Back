from rest_framework import serializers
from .models import Article, Comment


class ArticleListSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    user_profile_picture = serializers.ImageField(source='user.profile_picture', read_only=True)
    class Meta:
        model = Article
        fields = ('id', 'user_nickname', 'user_profile_picture', 'title', 'view', 'like_users', 'comment_set', 'created_at' )


class ArticleSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    user_profile_picture = serializers.ImageField(source='user.profile_picture', read_only=True)
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user',)
        
class ArticleCommentSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user_id.nickname', read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('article_id', 'user_id', )
