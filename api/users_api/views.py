from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializer import UserProfileSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import serializers
from rest_framework import renderers

from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from collections import Counter

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.account.adapter import get_adapter

from dj_rest_auth.registration.views import SocialLoginView, SocialLoginSerializer, SocialConnectView
from django.views.decorators.csrf import csrf_exempt


from google.oauth2 import id_token
from google.auth.transport import requests as google_auth_request

from urllib.parse import urlencode

from recommended_api.models import News
from recommended_api.serializer import NewsSerializer

from .utils import google_get_access_token, google_get_user_info, user_get_or_create, jwt_login


DOMAIN = "http://localhost:8000"
AUTH_GOOGLE_CALLBACK_URL = '/accounts/social/google/login/callback/'
AUTH_APPLE_CALLBACK_URL = '/accounts/social/apple/login/callback/'
CONNECT_GOOGLE_CALLBACK_URL = '/users/social/google/connect/'
CONNECT_APPLE_CALLBACK_URL = '/users/social/apple/connect/'


# Like unlike api view

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def like(request, news_id):
    try:
        user_profile = UserProfile.objects.get(account_id=request.user.pk)
    except UserProfile.DoesNotExist:
        return JsonResponse({"message": "This account does not exist"}, status=404)

    try:
        queryNewsData = News.objects.get(id=news_id)
    except News.DoesNotExist:
        return JsonResponse({"message": "This news does not exist"}, status=404)

    if news_id in user_profile.liked:
        return JsonResponse({"message": "already liked", "liked": queryNewsData.liked, "unliked": queryNewsData.unliked}, status=208)

    user_profile.liked.append(news_id)

    queryNewsData.liked = queryNewsData.liked + 1

    if news_id in user_profile.unliked:
        user_profile.unliked.remove(news_id)
        queryNewsData.unliked = queryNewsData.unliked - 1

    user_profile.save()
    queryNewsData.save()

    return JsonResponse({"message": "like Updated", "liked": queryNewsData.liked, "unliked": queryNewsData.unliked},
                        status=201)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def unlike(request, news_id):
    try:
        user_profile = UserProfile.objects.get(account_id=request.user.pk)
    except UserProfile.DoesNotExist:
        return JsonResponse({"message": "This account does not exist"}, status=404)

    try:
        queryNewsData = News.objects.get(id=news_id)
    except News.DoesNotExist:
        return JsonResponse({"message": "This news does not exist"}, status=404)

    if news_id in user_profile.unliked:
        return JsonResponse({"message": "already unliked", "liked": queryNewsData.liked, "unliked": queryNewsData.unliked}, status=208)

    user_profile.unliked.append(news_id)

    queryNewsData.unliked = queryNewsData.unliked + 1

    if news_id in user_profile.liked:
        user_profile.liked.remove(news_id)
        queryNewsData.liked = queryNewsData.liked - 1

    user_profile.save()
    queryNewsData.save()

    return JsonResponse({"message": "unlike Updated", "liked": queryNewsData.liked, "unliked": queryNewsData.unliked},
                        status=201)


# Get user profile api view


@api_view(['GET'])
def get_others_profile(request, id):
    queryData = UserProfile.objects.get(account_id=id)
    serializer = UserProfileSerializer(queryData)
    return JsonResponse(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    try:
        user_profile = UserProfile.objects.get(account_id=request.user.pk)
    except UserProfile.DoesNotExist:
        return JsonResponse({"message": "This account does not exist"}, status=204)
    serializer = UserProfileSerializer(user_profile)
    return JsonResponse(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    try:
        userQueryData = UserProfile.objects.get(account_id=request.user.pk)
        request.data['account_id'] = request.user.pk
        serializer = UserProfileSerializer(userQueryData, data=request.data)
    except UserProfile.DoesNotExist:
        request.data['account_id'] = request.user.pk
        serializer = UserProfileSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def more_topics(request):
    userQueryData = UserProfile.objects.get(account_id=request.user.pk)
    userSerializer = UserProfileSerializer(userQueryData)

    tagsFollowing = userSerializer.data['interests']
    newsQueryData = News.objects.all()
    tagsList = set()

    for news in newsQueryData:
        newsSerializer = NewsSerializer(news)
        articleTags = newsSerializer.data['entities']
        articleTags = articleTags.keys()

        for tag in articleTags:
            if tag not in tagsFollowing:
                tagsList.add(tag)

    tagsList = list(tagsList)
    return JsonResponse({"more_topics": tagsList}, status=200)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_interest(request):
    queryData = UserProfile.objects.get(account_id=request.user.pk)
    serializer = UserProfileSerializer(queryData)

    preferenceList = serializer.data['interests']
    addUserInterests = request.data.get('add_user_interests', None)
    removeUserInterests = request.data.get('remove_user_interests', None)

    if addUserInterests:
        for interest in addUserInterests:
            if interest not in preferenceList:
                preferenceList[interest] = 1

    elif removeUserInterests:
        for interest in removeUserInterests:
            if interest in preferenceList:
                del preferenceList[interest]

    else:
        return JsonResponse({"message": "Something went wrong!"}, status=400)

    preferenceList = dict(Counter(preferenceList).most_common(500))

    serializer = UserProfileSerializer(queryData, data=serializer.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "Interests Updated"}, status=201)
    return JsonResponse(serializer.errors, status=400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_read_interest(request, newsid):
    queryData = UserProfile.objects.get(account_id=request.user.pk)
    serializer = UserProfileSerializer(queryData)

    newsQueryData = News.objects.get(id=newsid)
    newsSerializer = NewsSerializer(newsQueryData)

    preferenceList = serializer.data['interests']
    articleTags = newsSerializer.data['entities']

    for key, value in articleTags.items():
        value = int(value)
        if key in preferenceList:
            preferenceList[key] += value
        else:
            preferenceList[key] = value

    preferenceList = dict(Counter(preferenceList).most_common(500))

    readList = serializer.data['read']
    readList.append(newsid)

    serializer = UserProfileSerializer(queryData, data=serializer.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "Interests and read lists updated"}, status=201)
    return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_interests(request):
    try:
        user_profile = UserProfile.objects.get(account_id=request.user.pk)
    except UserProfile.DoesNotExist:
        return JsonResponse({"message": "This account does not exist"}, status=204)
    serializer = UserProfileSerializer(user_profile)
    tags_following = serializer.data['interests']
    interests = list(tags_following)
    return JsonResponse({"interests": interests}, status=200)


from .mixins import ApiErrorsMixin, PublicApiMixin, ApiAuthMixin


class GoogleConnect(SocialConnectView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer
    callback_url = "{}{}".format(DOMAIN, CONNECT_GOOGLE_CALLBACK_URL)
    
    
class GoogleLogin(SocialLoginView):
    renderer_classes = [renderers.JSONRenderer]
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer
    callback_url = "{}{}".format(DOMAIN, AUTH_GOOGLE_CALLBACK_URL)

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)
    

class AppleConnect(SocialConnectView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer
    callback_url = "{}{}".format(DOMAIN, CONNECT_APPLE_CALLBACK_URL)
    
    
class AppleLogin(SocialLoginView):
    adapter_class = AppleOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer
    callback_url = "{}{}".format(DOMAIN, AUTH_APPLE_CALLBACK_URL)

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)
    

