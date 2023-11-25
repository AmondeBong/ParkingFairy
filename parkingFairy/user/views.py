from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserModel
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def login(request):
    return render(request, 'Login/index.html')


@csrf_exempt
def index(request):
    if request.method == 'GET':
        return render(request, 'SignUp/index.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pswd1')
        check_pswd = request.POST.get('pswd2')
        email = request.POST.get('email')
        birthday_year = request.POST.get('yy')
        birthday_month = request.POST.get('mm')
        birthday_date = request.POST.get('dd')
        gender = request.POST.get('gender')
        check_email = request.POST.get('check_email')
        mobile = request.POST.get('mobile')

        if password != check_pswd:
            return render(request, 'SignUp/alert.html')
            # 비밀번호가 같지않으면 alert
        else:
            exist_user = UserModel.objects.filter(email=email)
            if exist_user:
                return render(request, 'SignUp/alert3.html')
                # 존재하는 아이디면 alert
            else:
                new_user = UserModel()
                new_user.username = username
                new_user.password = password
                new_user.email = email
                new_user.birthday_year = birthday_year
                new_user.birthday_month = birthday_month
                new_user.birthday_date = birthday_date
                new_user.gender = gender
                new_user.check_email = check_email
                new_user.mobile = mobile

                new_user.save()
                return redirect('/user/login/')
