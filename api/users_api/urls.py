from django.urls import path,include
from dj_rest_auth.registration.views import (
    SocialAccountListView, SocialAccountDisconnectView
)
from . import views
from django.contrib import admin
# from .views import UserProfileView

urlpatterns = [
        
    # users path
    path('profiles/',views.get_profile ),
    path('profiles/<int:id>',views.get_others_profile ),
    path('profiles/update/',views.update_profile ),
    path('profiles/interests',views.get_user_interests),
    path('profiles/updateinterest',views.update_interest ),
    path('profiles/updatereadinterest/<int:newsid>', views.update_read_interest),
    path('moretopics', views.more_topics),

    # Like or unlike path
    path('like/<int:news_id>',views.like),
    path('unlike/<int:news_id>',views.unlike),
    
    path('social/facebook/login/', views.FacebookLogin.as_view(), name='facebook_login'),
    path('social/facebook/connect/', views.FacebookConnect.as_view(), name='facebook_connect'),
    path('social/google/login/', views.GoogleLogin.as_view(), name='google_login'),
    path('social/google/connect/', views.GoogleConnect.as_view(), name='google_connect'),
    path('social/apple/login/', views.AppleLogin.as_view(), name='apple_login'),
    path('social/apple/connect/', views.AppleConnect.as_view(), name='apple_connect'),
]
urlpatterns += [
    path('social/accounts/', SocialAccountListView.as_view(), name='social_account_list'),
    path('social/accounts/<int:pk>/disconnect/', SocialAccountDisconnectView.as_view(), 
        name='social_account_disconnect')
]