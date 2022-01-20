from django.contrib import admin
from django.urls import path,include
from .views import UserDetailView


urlpatterns = [
    path('admin/', admin.site.urls),
    # accounts path
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/registration/', include('dj_rest_auth.registration.urls')),
    path('accounts/info', UserDetailView.as_view()),

    path('accounts/social/', include('allauth.urls')),
    
    # Users profile path
    path('users/', include('users_api.urls')),
    
    # Categories path
    path('categories/', include('categories_api.urls')),

    # recommended path
    path('news/', include('recommended_api.urls')),
    
]
