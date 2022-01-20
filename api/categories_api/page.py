from django.core.paginator import Paginator

def paginate (request, data):
    paginator = Paginator(data, 9)
    page = request.GET.get('page', 1)
    try:
        data = paginator.page(page)
    except EmptyPage:
        data = []

    return data