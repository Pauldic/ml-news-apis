from .serializer import NewsSerializer
from django.core.paginator import Paginator, EmptyPage
from rest_framework import pagination, generics

def similar_news (articleEntities, all_news_data):    
    articles = []
    similarArticle = []
    for key, news in all_news_data.items():
        entitiesList = news['entities']
        matchScore = 0
        for entity in articleEntities:                  
            idx = find_index(entitiesList, lambda item: item[0] == entity[0])
            if idx:
                article = entitiesList[idx]
                matchScore += min(entity[1], article[1])                    
        similarArticle.append([matchScore, key])
    
    similarArticle.sort(reverse=True)
    for _, article in zip(range(3), similarArticle):
        news = all_news_data[article[1]]
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
    return articles

def paginate (request, data):
    page = request.GET.get('page', 1)
    count = request.GET.get('count', 10)

    paginator = Paginator(data, count)
    try:
        data = paginator.page(page)
    except EmptyPage:
        data = []

    return data

def find_index(l, f):
    return next((i for i in range(len(l)) if f(l[i])), None)

class News15Pagination(pagination.PageNumberPagination):
    page_size = 15  # the no. of company objects you want to send in one go
