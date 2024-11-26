from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.conf import settings
from django.db.models import Count
from django.http import JsonResponse


from django.shortcuts import get_object_or_404

from .serializers import EndingListSerializer, EndingSerializer, MovieListSerializer, MovieSerializer, EndingCommentSerializer
from .models import Ending, Movie, Comment
from openai import OpenAI
from django.contrib.auth import get_user_model


# @permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def ending_list(request):
    if request.method == 'GET':
        endings = Ending.objects.all()
        serializer = EndingListSerializer(endings, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EndingSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = request.user
            # 게시글 작성시 토큰 개수 증가
            user.token += 3
            user.save()
            serializer.save(user_id=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def ending_detail(request, ending_pk):
    ending = Ending.objects.get(pk=ending_pk)
    if request.method == 'GET':
        ending.view += 1
        ending.save()
        serializer = EndingSerializer(ending)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        ending.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.filter(is_selected=True)
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        if not request.user.is_admin:
            error_data = {
                'Access Denied': ['관리자만 접근 가능합니다.']
            }
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET',])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
@api_view(['GET', 'POST'])
def comment_list(request, ending_pk):
    if request.method == 'GET':
        comments = Comment.objects.filter(ending_id=ending_pk)
        serializer = EndingCommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        ending = get_object_or_404(Ending, pk=ending_pk)
        serializer = EndingCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # 현재 유저의 토큰정보 확인
            user = request.user
            # 댓글 작성시 토큰 개수 증가
            user.token += 1
            user.save()
            serializer.save(user_id=user, ending_id=ending)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['DELETE', 'PUT'])
def comment_manage(request, comment_pk):
    if request.method == 'DELETE':
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        comment = get_object_or_404(Comment, pk=comment_pk)
        serializer = EndingCommentSerializer(instance = comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
    

@api_view(['POST',])
def generate_alt_ending(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    # 현재 유저의 토큰정보 확인
    user = request.user
    if user.token <= 4:
        raise PermissionDenied("사용 가능한 토큰이 부족합니다.")
    
    # 프롬프트 작성전 토큰 수 감소
    user.token -= 5
    user.save()

    # 프롬프트 작성 시작
    user_prompt = request.data.get('prompt','')
    prev_alt_ending = request.data.get('content','')
    client = OpenAI(api_key=settings.OPENAI_SECRET_KEY)
    movie_title = movie.title
    movie_plot = movie.plot

    if not prev_alt_ending:
        prompt_for_gpt = f"Plot summary: {movie_plot}\n\nGenerate an alternative ending for the movie {movie_title}. The alternative ending should diverge from the original conclusion with the given environment after. You will answer full plot of alternative ending by user input. Return plot only. If user input is irrelevant with movie, than return error message. NEVER ANSWER IN ENGLISH. PLEASE ANSWER IN KOREAN."        
    else:
        prompt_for_gpt = f"Plot summary: {movie_plot}\n\nYour Client is not content with your output. Generate an alternative ending for the movie {movie_title} again. The alternative ending(your result) should include the feedback from your client. You will answer full plot of alternative ending. Return plot only. If user input is irrelevant with movie or previous alternative ending, than return error message. NEVER ANSWER IN ENGLISH. PLEASE ANSWER IN KOREAN. The alternative ending you created is below. If previous alternative ending has error message, then you can skip it.\n\n{prev_alt_ending}"        
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": '타노스가 어떤 일이 있어야 핑거스냅을 하지 못하게 될까?'},
                {"role": "assistant", "content": '''
타노스가 아스가르드의 우주선에 타 있다. 그는 우주선 안에 숨겨진 테서랙트에 있는 스페이스 스톤을 찾기 위해 공격을 감행한다. 타노스는 헐크와 토르를 무자비하게 처치하며 승리를 거두고, 테서랙트를 손에 넣는다. 이로 인해 아스가르드의 잔존자들은 우주에 흩어지게 된다.

와중, 뉴욕에서 닥터 스트레인지와 토니 스타크는 타노스의 추종자들인 에보니 모와 칼 오브시디언에게 공격당한다. 이 과정에서 스파이더맨이 그들을 구출하고, 함께 타노스의 군대에 대한 저항을 한다.

한편, 아스가르드의 잔여 팀과 가디언즈 오브 갤럭시의 토르는 새로운 무기를 찾기 위해 움다르의 대장간으로 향한다. 그러나 타노스는 이미 멀리 떨어진 지구에서 자신의 목표를 향해 나아가고 있다.

어벤져스는 와칸다에서 비전과 그들의 동맹을 만난다. 어벤져스는 비전의 이마에 박혀 있는 마인드 스톤이 타노스의 손에 빠지면 큰 재앙이 일어날 것을 염려한다. 
                 
따라서 어벤져스와 그들의 동맹들은 타노스의 계획을 막기 위해 고대의 힘을 찾아 나선다. 닥터 스트레인지는 시간여행을 통해 과거로 돌아가고, 인피니티 스톤의 힘을 막을 보호막을 생성한다. 타노스가 공격할 때 보호막 덕분에 그의 힘이 제한되며, 어벤져스는 힘을 합쳐 타노스를 압도한다.

결국 타노스는 자신의 스톤들을 잃고, 핑거스냅을 할 수 없는 상황에 처한다. 어벤져스는 새로운 연합을 구성하고 타노스를 감금한 뒤, 잃어버린 동료들을 위해 새로운 싸움을 준비한다. 이제 어벤져스는 다시 평화를 되찾고 서로 간의 유대감을 강화하는 시간을 가지게 된다.
                 '''},
                {"role": "user", "content": "모아나가 한국 울릉도에 있는 우산국의 족장의 딸이었다면?"},
                {"role": "assistant", "content": '''
모아나는 우산국 족장의 딸이다. 어느 날부터인가 바다의 환경이 안 좋아지기 시작하고, 바다에 사는 모든 생명체들이 위험에 빠지기 시작한다. 우산국의 사람들은 어떻게든 되겠지라며 무시하고 있다. 그러나 모아나는 이런 상황을 받아들이지 않고, 우산국의 전설 속에 등장하는 바다의 수호신이자 그녀의 조상인 전설적인 인물 '이순신'을 찾기 위해 모험을 떠난다. 
                 
바다를 항해하며, 그녀는 반신반인 같은 존재인 '이사부'를 우연히 만나게 된다. 처음에는 이사부가 그녀를 거부하지만, 모아나의 끈질긴 의지와 용기는 그를 감동시킨다.

두 사람은 협력하여 왜놈의 침략과 다양한 도전을 극복하며, 울릉도를 지켜야 하는 이유와 자신의 정체성을 깨닫는다. 이 과정에서 그들은 울릉도와 그 주변의 생태계와 문화에 대한 깊은 이해를 쌓아간다.

그러던 중, 이사부는 모아나에게 그들의 역사와 바다의 중요성을 설명하며, 전통적인 항해 기술과 고대 우산국의 문화유산에 대한 지식을 공유한다. 모아나는 자신의 조상들이 바다와 어떻게 조화롭게 살아왔는지를 깨닫고, 그 문화유산을 되살리기로 결심한다.

결국 모아나는 바다의 저주를 풀기 위해, 전설의 신물과 함께 울릉도의 중심부에 있는 신성한 돌에 도착한다. 여기에서 모아나는 사람들의 마음과 자연의 조화를 이루는 의식을 거행하게 된다. 이 과정에서 울릉도의 생명력이 회복되고, 사람들이 바다와 조화롭게 살아갈 수 있는 새로운 균형이 이루어진다.

모아나가 울릉도로 돌아가자 그녀의 사람들은 진정한 영웅으로서 그녀를 환영했으며, 그녀는 울릉도의 새로운 모험과 항해 문화를 이끌어가는 지도자가 된다. 바다를 향한 경외심과 조상의 전통을 계승하는 모아나의 모습은 우산국의 사람들이 다시 한 번 바다와 함께 꿈꿀 수 있는 새로운 시작이 된다.

이렇게 모아나는 자신의 정체성을 찾고, 우산국의 전통과 바다의 힘을 재발견하여 새로운 시대를 열어간다.
                '''},
                { "role": "system", 'content':prompt_for_gpt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=1500,
            n=1,
            temperature=0.9
        )
        gpt_response = response.choices[0].message.content
    except Exception as e:
        return Response({'error': f"Failed to communicate with GPT: {str(e)}", 'user_token': user.token}, status=500)
    
    # Return the GPT response
    return Response({'alt_ending': gpt_response, 'user_token' : user.token})

@api_view(['POST'])
def likes(request, ending_pk):
    ending = get_object_or_404(Ending, pk=ending_pk)
    # dislike 제거
    if request.user in ending.dislike_users.all():
        ending.dislike_users.remove(request.user)
    
    if request.user in ending.like_users.all():
        ending.like_users.remove(request.user)
        is_liked = False
    else:
        ending.like_users.add(request.user)
        is_liked = True
    ending.save()
    
    context = {
        'is_liked': is_liked,
        'is_disliked': False
    }
    return Response(context)

@api_view(['POST'])
def dislikes(request, ending_pk):
    ending = get_object_or_404(Ending, pk=ending_pk)
    # like 제거
    if request.user in ending.like_users.all():
        ending.like_users.remove(request.user)
    
    if request.user in ending.dislike_users.all():
        ending.dislike_users.remove(request.user)
        is_disliked = False
    else:
        ending.dislike_users.add(request.user)
        is_disliked = True
    ending.save()
    
    context = {
        'is_liked': False,
        'is_disliked': is_disliked
    }
    return Response(context)

@api_view(['GET'])
def GetUserRanking(request):
    user_ranking = (
        Ending.objects.values("user_id__id",)
        .annotate(total_likes=Count("like_users"))
        .order_by("-total_likes")[:3]
    )
    User = get_user_model()
    user_dict = dict()
    for rank, user in enumerate(user_ranking):
        user_instance = get_object_or_404(User, pk=user['user_id__id'])
        user_dict[rank+1] = {
            'user_name': user_instance.nickname,
            'total_likes': user['total_likes'],
            'user_id': user['user_id__id'],
            'profile_picture': user_instance.profile_picture.url
            }
    return JsonResponse(user_dict, safe=True)


@api_view(['GET'])
def GetEndingRanking(request):
    most_liked_article = (
        Ending.objects.annotate(like_count=Count("like_users")-Count("dislike_users"))
        .order_by("-like_count")[:6]
    )
    ending_dict = dict()

    for rank, article in enumerate(most_liked_article):
        ending_dict[rank+1] = {
            'movie': article.movie_id.title,
            'prompt': article.prompt,
            'like_count': article.like_count,
            'ending_id': article.id
        }
    
    return JsonResponse(ending_dict, safe=True)

@api_view(['GET', 'PUT'])
def movie_select(request):
    if not request.user.is_admin:
        error_data = {
            'Access Denied': ['관리자만 접근 가능합니다.']
        }
        return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        selected_movies = request.data.get('selected_movies', [])
        # 모든 영화의 선택 상태를 먼저 False로 설정
        Movie.objects.all().update(is_selected=False)
        # 선택된 영화들만 True로 업데이트
        Movie.objects.filter(id__in=selected_movies).update(is_selected=True)
        return Response({'message': '영화 선택이 업데이트되었습니다.'}, status=status.HTTP_200_OK)
