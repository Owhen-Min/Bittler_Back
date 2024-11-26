from django.urls import path, include
from accounts import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/v1/accounts/', include('dj_rest_auth.urls')),
    path('api/v1/accounts/signup/', include('dj_rest_auth.registration.urls')),
    path('api/v1/movies/', include('moviearticles.urls')),
    path('api/v1/communities/', include('communityarticles.urls')),
    path('api/v1/accounts/<int:user_pk>/', views.GetProfile),
    path('api/v1/accounts/info/<int:user_pk>/', views.GetInfo),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
