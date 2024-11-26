from django.urls import path
from . import views


urlpatterns = [
    path('', views.article_list),
    path('<int:article_pk>/', views.article_detail),
    path('<int:article_pk>/comments/', views.comment_list),
    path('<int:article_pk>/likes/', views.likes),
    path('<int:comment_pk>/comments/manage/', views.comment_manage),
]
