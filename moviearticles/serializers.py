from rest_framework import serializers
from .models import Ending, Movie, Comment

class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster',)
        
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class EndingListSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user_id.nickname', read_only=True)
    user_profile_picture = serializers.ImageField(source='user_id.profile_picture', read_only=True)
    like_count = serializers.SerializerMethodField()
    class Meta:
        model = Ending
        fields = ('id', 'prompt', 'user_nickname', 'user_profile_picture', 'view', 'comment_set', 'like_count' )

    def get_like_count(self, obj):
        return max(0, obj.like_users.count() - obj.dislike_users.count())



class EndingSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user_id.nickname', read_only=True)
    user_profile_picture = serializers.ImageField(source='user_id.profile_picture', read_only=True)
    movie_info = MovieSerializer(source='movie_id', read_only=True)
    class Meta:
        model = Ending
        fields = '__all__'
        read_only_fields = ('id', 'user_id',)
        

class EndingCommentSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user_id.nickname', read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'ending_id', 'user_id', )