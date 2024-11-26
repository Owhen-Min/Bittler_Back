from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list),
    path('<int:movie_pk>/', views.movie_detail),
    path('<int:movie_pk>/altends/', views.generate_alt_ending),
    path('altends/', views.ending_list),
    path('altends/<int:ending_pk>/', views.ending_detail),
    path('altends/<int:ending_pk>/comments/', views.comment_list),
    path('altends/<int:comment_pk>/comments/manage/', views.comment_manage),
    path('altends/<int:ending_pk>/likes/', views.likes),
    path('altends/<int:ending_pk>/dislikes/', views.dislikes),
    path('ranking/user/', views.GetUserRanking),
    path('ranking/ending/', views.GetEndingRanking),
    path('select/', views.movie_select),
]