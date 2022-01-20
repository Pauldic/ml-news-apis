from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Category
from .page import paginate
from .serializer import CategorySerializer
from rest_framework.decorators import api_view,permission_classes
from django.http import HttpResponse, JsonResponse


@api_view(['GET'])
def get_all_categories(request):
    queryset = Category.objects.order_by('serial')
    serializer = CategorySerializer(queryset, many=True)
    #return Response()
    return JsonResponse({'categories': serializer.data})


@api_view(['GET'])
def get_top_categories(request):
    if request.method == 'GET':
        data = Category.objects.all()
        ctgs = paginate(request, data)
        serializer = CategorySerializer(ctgs, many=True)
        return JsonResponse({'top_categories': serializer.data})



