from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import datetime
import argparse
import io
import os
import torch
import json

DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S-%f"


def index(request):

    return render(request, 'Main/index.html')
# 메인 페이지 요청


def error_404_view(request, exception):
    return HttpResponseNotFound("The page is note found!")
# 404 화면 출력


def login(request):
    return render(request, 'Login/index.html')
# Create your views here.


def signup(request):
    return render(request, 'SignUp/index.html')


@csrf_exempt
def detect(request):
    if request.method == "POST":  # request method 가 POST 일경우
        if "file" not in request.FILES:  # 받아오는 타입이 파일이 아닐경우, 다시 돌아가기
            return render(request, 'Main/index.html')
        file = request.FILES["file"]  # 받아오는 타입이 파일일 경우 그대로 받아오기

        if not file:  # 파일이 아예 없을 경우 경고 보내기
            return render("alert.html")

        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))

        model = torch.hub.load('yolov5', 'custom',
                               path='parkingFairy.pt', source='local')

        model.eval()

        results = model([img])
        context = {'data': results.pandas().xyxy[0].to_json(orient="records")}
        # json 형태로 저장된 정보

        # results.render()  # results.imgs 를 boxes and labels로 업데이트 함
        # now_time = datetime.datetime.now().strftime(DATETIME_FORMAT)  # 현재의 날짜 정보 불러오기
        # file_path = f"../static/result_json/{now_time}.json"
        # 현재 날짜 정보가 이름인 이미지 생성
        # img_savepath = f"../static/result_picture/{now_time}.png"
        # Image.fromarray(results.ims[0]).save(img_savepath)  # 업데이트된 result.img를 현재 날짜 정보로 저장

        return render(request, 'result/detect.html', context)

    return render(request, 'Main/index.html')  # 이미지 불러오기에 실패할 경우 메인 페이지
