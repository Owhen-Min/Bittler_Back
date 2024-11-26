from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from communityarticles.serializers import ArticleCommentSerializer, ArticleSerializer
from moviearticles.serializers import EndingCommentSerializer, EndingSerializer

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(max_length=20, required=True)
    
    def validate_nickname(self, nickname):
        if User.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError("이미 사용 중인 닉네임입니다.")
        return nickname
    
    def save(self, request):
        user = super().save(request)
        nickname = self.data.get('nickname')
        first_name = self.data.get('first_name')
        is_admin = self.data.get('is_admin')
        user.nickname = nickname
        user.first_name = first_name
        user.is_admin = is_admin
        user.save()
        return user

class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'nickname', 'profile_picture', 'join_date', 'token', 'is_admin')
        read_only_fields = ('pk', 'username', 'join_date', )

class UserRankingSerializer(ModelSerializer):
    total_likes = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('pk', 'profile_picture', 'nickname', 'total_likes')

    def get_total_likes(self, obj):
        return max(0, obj.like_articles.count() - obj.dislike_articles.count())


class UserInfoSerializer(serializers.ModelSerializer):
    article_comment_count = serializers.SerializerMethodField()
    ending_comment_count = serializers.SerializerMethodField()
    article_like_count = serializers.SerializerMethodField()
    ending_like_count = serializers.SerializerMethodField()
    article_count = serializers.SerializerMethodField()
    ending_count = serializers.SerializerMethodField()
    recent_articles = serializers.SerializerMethodField()
    recent_endings = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'nickname', 'join_date', 'token', 'profile_picture', 'article_comment_count', 'ending_comment_count', 'article_like_count', 'ending_like_count', 'article_count', 'ending_count', 'recent_articles', 'recent_endings')

    def get_article_comment_count(self, obj):
        return obj.comment_articles.count()  # 해당 유저의 댓글 개수 (ArticleComment)

    def get_ending_comment_count(self, obj):
        return obj.comment_endings.count()  # 해당 유저의 댓글 개수 (EndingComment)

    def get_article_like_count(self, obj):
        return obj.like_articles.count()  # 해당 유저의 좋아요 개수 (Article)

    def get_ending_like_count(self, obj):
        return obj.like_endings.count()  # 해당 유저의 좋아요 개수 (Ending)

    def get_article_count(self, obj):
        return obj.Community_Article.count()  # 해당 유저의 게시글 개수 (Article)

    def get_ending_count(self, obj):
        return obj.Ending.count()  # 해당 유저의 대체 결말 개수 (Ending)

    def get_recent_articles(self, obj):
        recent_articles = obj.Community_Article.order_by('-created_at')[:5]  # 최근 5개 게시글
        return [
            {
                'id': article.id,
                'title': article.title,
                'created_at': article.created_at,
            } for article in recent_articles
        ]
    
    def get_recent_endings(self, obj):
        recent_endings = obj.Ending.order_by('-created_at')[:5]  # 최근 5개 대체 결말
        return [
            {
                'id': ending.id,
                'prompt': ending.prompt,
                'created_at': ending.created_at,
            } for ending in recent_endings
        ]