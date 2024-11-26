from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import ArticleListSerializer, ArticleSerializer, ArticleCommentSerializer
from .models import Article, Comment


@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # 현재 유저의 토큰정보 확인
            user = request.user
            # 게시글 작성시 토큰 개수 증가
            user.token += 3
            user.save()
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE', 'PUT'])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'GET':
        article.view += 1
        article.save()
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        serializer = ArticleSerializer(instance = article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)

# @login_required
@api_view(['GET', 'POST'])
def comment_list(request, article_pk):
    if request.method == 'GET':
        comments = Comment.objects.filter(article_id=article_pk)
        serializer = ArticleCommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        article = get_object_or_404(Article, pk=article_pk)
        serializer = ArticleCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # 현재 유저의 토큰정보 확인
            user = request.user
            # 댓글 작성시 토큰 개수 증가
            user.token += 1
            user.save()
            serializer.save(user_id=user, article_id=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

@api_view(['DELETE', 'PUT'])
def comment_manage(request, comment_pk):
    if request.method == 'DELETE':
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        comment = get_object_or_404(Comment, pk=comment_pk)
        serializer = ArticleCommentSerializer(instance = comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)

    
# @login_required
@api_view(['POST'])
def likes(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
        article.save()
        is_liked = False
    else:
        article.like_users.add(request.user)
        article.save()
        is_liked = True
    context = {
        'is_liked': is_liked,
    }
    return Response(context)