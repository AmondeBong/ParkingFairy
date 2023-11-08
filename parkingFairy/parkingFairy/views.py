from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound


def index(request):

    return render(request, 'Main/index.html')
# 메인 페이지 요청


def error_404_view(request, exception):
    return HttpResponseNotFound("The page is note found!")
# 404 화면 출력
