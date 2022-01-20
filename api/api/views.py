from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, JsonResponse


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,*args, **kwargs):
        return JsonResponse({
                            "account_id": request.user.pk, 
                            "email": request.user.email, 
                            "username": request.user.username,
                            "created_at": request.user.date_joined,                           
                            })