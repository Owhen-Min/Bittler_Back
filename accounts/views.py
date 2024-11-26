from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from django.shortcuts import get_object_or_404
from .serializers import UserProfileSerializer, UserInfoSerializer

@api_view(['GET', 'PUT'])
def GetProfile(request, user_pk):
    if user_pk == 0:
        user = get_object_or_404(User, pk = request.user.pk)
    else:
        user = get_object_or_404(User, pk=user_pk)
    if request.method == 'GET':
        serializer = UserProfileSerializer(user)
        return Response(data=serializer.data)

    elif request.method == 'PUT':
        serializer = UserProfileSerializer(instance = user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        
@api_view(['GET'])
def GetInfo(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    if request.method == 'GET':
        serializer = UserInfoSerializer(user)
        return Response(data=serializer.data)