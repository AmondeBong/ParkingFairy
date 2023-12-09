from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import datetime
import argparse
import io
import os
import torch
import json
from django.contrib.auth import get_user_model
from .mqtt_client import mqtt_connect

small = [0, 1, 4, 7, 9, 10, 11, 15, 18, 45, 46, 54, 59, 61, 73, 74]
middle = [2, 5, 6, 8, 12, 13, 14, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
          32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 47, 48, 49, 50, 51, 52, 53, 57, 60, 62, 63]
bit = [55, 56, 58, 64, 65, 66, 67, 68, 69, 70, 71, 72]


def index(request):

    return render(request, 'Main/index.html')
# 메인 페이지 요청


def error_404_view(request, exception):
    return HttpResponseNotFound("The page is note found!")
# 404 화면 출력


@csrf_exempt
@login_required
def reservation(request):
    if request.method == "GET":
        return render(request, 'reservation/index.html')
    if request.method == "POST":  # request method 가 POST 일경우
        if "file" not in request.FILES:  # 받아오는 타입이 파일이 아닐경우, 다시 돌아가기
            return render(request, 'reservation/index.html')
        file = request.FILES["file"]  # 받아오는 타입이 파일일 경우 그대로 받아오기

        if not file:  # 파일이 아예 없을 경우 경고 보내기
            return render("alert.html")

        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))

        model = torch.hub.load('yolov5', 'custom',
                               path='parkingFairy.pt', source='local')

        model.eval()

        results = model([img])

        data = results.pandas().xyxy[0].to_json(orient="records")
        data = data[1:len(data)-1]

        result = json.loads(data)
        car = {}

        car['name'] = result['name']

        if result['class'] in small:
            car['size'] = '소형'
        elif result['class'] in middle:
            car['size'] = '중형'
        else:
            car['size'] = '대형'

        user = request.user
        user.car = car
        user.save()

        results.render()  # results.imgs 를 boxes and labels로 업데이트 함
        # now_time = datetime.datetime.now().strftime(DATETIME_FORMAT)  # 현재의 날짜 정보 불러오기
        img_path = f"/srv/ParkingFairy/parkingFairy/static/result_image/{user.username}.png"
        Image.fromarray(results.ims[0]).save(
            img_path)  # 업데이트된 result.img를 현재 날짜 정보로 저장

        file_path = f"../static/result_json/{user.username}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(car, f)

        img_path_2 = f"/static/result_image/{user.username}.png"
        context = {'name': car['name'], 'size': car['size'], 'img': img_path_2}

        return render(request, 'result/detect.html', context)

    return render(request, 'Main/index.html')  # 이미지 불러오기에 실패할 경우 메인 페이지


@csrf_exempt
def detect(request):
    if request.method == "POST":  # request method 가 POST 일경우
        if "file" not in request.FILES:  # 받아오는 타입이 파일이 아닐경우, 다시 돌아가기
            return render(request, 'reservation/index.html')
        file = request.FILES["file"]  # 받아오는 타입이 파일일 경우 그대로 받아오기

        if not file:  # 파일이 아예 없을 경우 경고 보내기
            return render("alert.html")

        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))

        model = torch.hub.load('yolov5', 'custom',
                               path='parkingFairy.pt', source='local')

        model.eval()

        results = model([img])

        data = results.pandas().xyxy[0].to_json(orient="records")
        for i in range(5):
            del data[i]

        context = {'data': data}

        # json 형태로 저장된 정보

        results.render()  # results.imgs 를 boxes and labels로 업데이트 함
        # now_time = datetime.datetime.now().strftime(DATETIME_FORMAT)  # 현재의 날짜 정보 불러오기
        file_path = f"parkingFairy/static/result_image/{user.username}.png"
        # Image.fromarray(results.ims[0]).save(img_savepath)  # 업데이트된 result.img를 현재 날짜 정보로 저장

        return render(request, 'result/detect.html', context)

    return render(request, 'Main/index.html')  # 이미지 불러오기에 실패할 경우 메인 페이지
