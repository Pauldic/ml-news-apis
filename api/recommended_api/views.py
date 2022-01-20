from collections import Counter
from functools import reduce
import random
from typing import Dict
import uuid
import datetime
import math

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import News
from users_api.models import UserProfile
from users_api.serializer import UserProfileSerializer
from .serializer import NewsSerializer
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse, JsonResponse
from django.db.models import F,Sum
from .helpers import similar_news, paginate, find_index, News15Pagination

# Create your views here.



class FeedNewsListView(generics.ListAPIView):
    
    def list(self, request):
        page_size = 15
        page_number = 1 if request.query_params.get('page') == None else int(request.query_params.get('page'))

        queryset = News.objects.all()[(page_number - 1) * page_size:(page_number * page_size)]
        serializer = NewsSerializer(queryset, many=True)
        page = serializer.data
        articles = []
        allNews = {news['id']:news for news in page}

        for news in page:            
            similarNews = similar_news(news['entities'], allNews)
            articleFormat = {
                'id': news['id'],
                'source': news['source'],
                'author': news['author'],
                'title': news['title'],
                'description': ("").join(news['description'].splitlines()[:5]),
                'url': news['url'],
                'urltoimage': news['urltoimage'],
                'publishedat': news['publishedat'],
                'updatedat': news['updatedat'],
                'entities': news['entities'],
                'liked':news['liked'],
                'unliked':news['unliked'],
                'similar_news': similarNews,
            }
            articles.append(articleFormat)

        random.shuffle(articles)
        total_news_count = News.objects.count()
        total_page = math.ceil(total_news_count / page_size)

        results = {'count': total_news_count, 'previous': None if page_number == 1 else 'news/?page=' + str(page_number), 'next': None if total_page <= page_number else 'news/?page=' + str(page_number + 1), 'results': articles}
        return JsonResponse(results, status = 200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommended(request):

    try:
        if request.method == 'GET':
            user = UserProfile.objects.get(account_id = request.user.pk)

            userID = user.account_id
            userInterests = user.interests
            userRead = user.read

            # Reading articles from database

            allNews = {}

            data = News.objects.all().exclude(id__in=userRead)
            data = paginate(request, data)
            
            for news in data:
                serializer = NewsSerializer(news)
                allNews[serializer.data['id']] = serializer.data

            entitiesPerArticle = [[news['entities'], news['id']] for (_,
                                news) in allNews.items()]

            similarArticle = []
            for (i, entitiesListEnum) in enumerate(entitiesPerArticle):
                matchedInterests = 0
                for interest in userInterests:
                    matchedInterests += min(userInterests[interest], entitiesListEnum[0].get(interest,0))

                similarArticle.append([matchedInterests, entitiesListEnum[1]])

            similarArticle.sort(reverse=True)
            articles = []
            for article in similarArticle:
                news = allNews[article[1]]
                articleFormat = {
                    'id': news['id'],
                    'source': news['source'],
                    'author': news['author'],
                    'title': news['title'],
                    'description': ("").join(news['description'].splitlines()[:5]),
                    'url': news['url'],
                    'urltoimage': news['urltoimage'],
                    'publishedat': news['publishedat'],
                    'updatedat': news['updatedat'],
                    'entities': news['entities'],                    
                    'liked':news['liked'],
                    'unliked':news['unliked'],
                    }

                articles.append(articleFormat)

            total_recommended_article = len(articles)
            results = {'user_id': userID, 'feeds': articles, 'total_recommended_article': total_recommended_article}
            return JsonResponse(results, status = 200)
    except:
        return JsonResponse({"message": "Something went wrong!"}, status = 400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_related_news(request, newsid):
    try:
        history = request.data.get("history")
        user = UserProfile.objects.get(account_id = request.user.pk)
        userID = user.account_id
        userRead = user.read
        userRead.append(newsid)

        newsData = News.objects.get(id = newsid)
        serializer = NewsSerializer(newsData)
        articleEntities = serializer.data['entities']

        # Reading articles from database

        data = News.objects.all()
        try:
            if history:                    
                history = history.split(',')
                data = data.exclude(id__in=history)[:1000]
        except Exception as ex:
            history = ''

        
        allNews = {}            
        for news in data:
            serializer = NewsSerializer(news)
            allNews[serializer.data['id']] = serializer.data      
        articles = similar_news(articleEntities, allNews)            
        results = {'user_id': userID, 'feeds': articles}
        return JsonResponse(results, status = 200)
    except:
        return JsonResponse({"message": "Something went wrong!"}, status = 400)



@permission_classes([IsAuthenticated])
class TrendingListView(generics.ListAPIView):
    pagination_class = News15Pagination
    def list(self, request):
        queryset = News.objects.all().annotate(total=F('liked') + F('unliked')).order_by('-total','-publishedat')
        serializer = NewsSerializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)
        response_list = self.get_paginated_response(page)
        return response_list

# Category wise news api view
@api_view(['GET'])
def get_news_by_category(request,category):
    try:
        queryNewsData = News.objects.filter(category__iexact=category).order_by('-publishedat') [:15]
        serializer = NewsSerializer(queryNewsData, many=True)
        return JsonResponse({"feeds":serializer.data}, status = 200)
    except:
        return JsonResponse({"message": "Something went wrong!"}, status = 400)

class NewsByTagsListView(generics.ListAPIView):
    pagination_class = News15Pagination

    def list(self, request, *args, **kwargs):     
        try:        
            tag = kwargs['tag']
            
            queryset = News.objects.filter(tags__icontains=tag).order_by('-publishedat')
            serializer = NewsSerializer(queryset, many=True)
            page = self.paginate_queryset(serializer.data)
            response_list = self.get_paginated_response(page)            
            return response_list
        except:
            return JsonResponse({"message": "Something went wrong!"}, status = 400)


@api_view(['GET'])
def popular_topics(request):
    try:
        # return top 100s topics
        all_news = News.objects.all().annotate(total=F('liked') + F('unliked')).order_by('-total','-publishedat')[:30]
        popular_topics_counter = Counter({})
        for news in all_news:
            news_serializer = NewsSerializer(news)
            news_tags = news_serializer.data['entities']
            popular_topics_counter = popular_topics_counter + Counter({str(item[0]):item[1] for item in news_tags})

        popular_topics_dict = dict(sorted(dict(popular_topics_counter).items(), key=lambda item: -item[1]))
        popular_topics_list = [item[0] for item in popular_topics_dict.items()]
        return JsonResponse({"popular_topics": popular_topics_list}, status=200)
    except Exception as ex:
        print(ex)
        return JsonResponse({"message": "Something went wrong!"}, status = 400)

@permission_classes([IsAuthenticated])
class UserPostListView(generics.ListAPIView):
    pagination_class = News15Pagination
    def list(self, request):
        try:
            account_id = request.user.pk
            print(account_id)
            userPostsQSet = News.objects.filter(user__account_id = account_id).order_by('-publishedat')
           
            serializer = NewsSerializer(userPostsQSet, many=True)            
            page = self.paginate_queryset(serializer.data)
            articles = []
            for news in page:                
                articleFormat = {
                    'id': news['id'],
                    'source': news['source'],
                    'author': news['author'],
                    'title': news['title'],
                    'description': ("").join(news['description'].splitlines()[:5]),
                    'url': news['url'],
                    'urltoimage': news['urltoimage'],
                    'publishedat': news['publishedat'],
                    'updatedat': news['updatedat'],
                    'entities': news['entities'],
                    'liked':news['liked'],
                    'unliked':news['unliked'],
                    'similar_news': [],
                }
                articles.append(articleFormat)
            response_list = self.get_paginated_response(articles)
            return response_list
           
        except Exception as ex:
            print(ex)
            return JsonResponse({"message": "Something went wrong!"}, status = 400)

# Category wise news api view
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def save_new_post(request):
    try:
        account_id = request.user.pk
        user = UserProfile.objects.get(account_id = account_id)        
        data = request.data        
        link = "/news/" + str(uuid.uuid4())
        source = "https://juggle.com"
        tagData = data.get('category').split(',')
        entities = [[item, 1] for item in tagData]
        tags = [tuple(item) for item in entities]
        expired = datetime.datetime.now() + datetime.timedelta(hours = int(data.get("hour")))
        newData = {
            "link" : link,
            "source" : source,
            "author" : str(user),
            "title" : data.get("title"),
            "small_description" : data.get("content"),
            "description" :  data.get("content"),
            "category" : '',
            "url" : source + link,
            "urltoimage" : data.get("image"),
            "entities" : entities,
            "tags" : tags,
            "expired" : expired,
            "user_id": account_id,
        }
        News.objects.create(**newData)

        return JsonResponse({"feeds":newData}, status = 200)
    except Exception as ex:
        print(ex)
        return JsonResponse({"message": "Something went wrong!"}, status = 400)
