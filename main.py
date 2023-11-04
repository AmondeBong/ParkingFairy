import argparse
import io
import os
from PIL import Image
import datetime

import torch
from flask import Flask, render_template, request, redirect, make_response
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S-%f"

app.debug = False

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler  # logging 핸들러
    file_handler = RotatingFileHandler(
        'dave_server.log', maxBytes=2000, backupCount=10)
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)


@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(error)
    return "<h1>해당 경로에 맞는 웹페이지가 없습니다.</h1>", 404


@app.route("/", methods=["GET", "POST"])  # 라우팅
def predict():
    if request.method == "POST":  # request method 가 POST 일경우
        if "file" not in request.files:  # 받아오는 타입이 파일이 아닐경우, 다시 돌아가기
            return redirect(request.url)
        file = request.files["file"]  # 받아오는 타입이 파일일 경우 그대로 받아오기

        if not file:  # 파일이 아예 없을 경우 경고 보내기
            return render_template("alert.html")

        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        results = model([img])
        api_code = results.pandas().xyxy[0].to_json(orient="records")
        # json 형태로 저장된 정보

        results.render()  # results.imgs 를 boxes and labels로 업데이트 함
        now_time = datetime.datetime.now().strftime(DATETIME_FORMAT)  # 현재의 날짜 정보 불러오기
        # file_path = f"static/result_json/{now_time}.json"
        # 현재 날짜 정보가 이름인 이미지 생성
        img_savename = f"static/result_picture/{now_time}.png"

        Image.fromarray(results.ims[0]).save(
            img_savename)  # 업데이트된 result.img를 현재 날짜 정보로 저장

        return render_template("result.html", api=api_code, img=img_savename)

    return render_template("index.html")  # 기본 화면은 index.html


@app.route("/result.js", methods=["GET", "POST"])
def page_chart():
    resp = make_response(render_template("result.js"))
    return resp


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=8100, type=int, help="port number")
    args = parser.parse_args()

    model = torch.hub.load('yolov5', 'custom',
                           path='parkingFairy.pt', source='local')

    model.eval()

    app.run(host="0.0.0.0", port=args.port)
