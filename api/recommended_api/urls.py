from django.urls import path,include
from . import views 
from .views import TrendingListView, NewsByTagsListView, FeedNewsListView, UserPostListView
from django.contrib import admin

urlpatterns = [
    # path('', views.get_news),
    path('', FeedNewsListView.as_view()),
    path('recommended', views.get_recommended),
    path('related/<int:newsid>', views.get_related_news),

    # path('trending', views.get_trending_news),
    path('trending', TrendingListView.as_view()),
    path('category/<str:category>', views.get_news_by_category),
    # path('tag/<str:tag>', views.get_news_by_tag),
    path('tag/<str:tag>', NewsByTagsListView.as_view()),
    path('popular/topics', views.popular_topics),
    path('userpost', UserPostListView.as_view()),
    path('post', views.save_new_post),
]