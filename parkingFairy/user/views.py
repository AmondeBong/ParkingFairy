from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import get_user_model


@csrf_exempt
def Login(request):
    if request.method == 'GET':
        return render(request, 'Login/index.html')
    elif request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        if not User.objects.filter(username=username).exists():
            return render(request, 'Login/alert2.html')

        authenticated_user = authenticate(username=username,
                                          password=password)
        if authenticated_user is not None:
            login(request, authenticated_user)

        else:
            return render(request, 'Login/alert.html')
        # else:
    return redirect('/')
    # 사용자 인증 실패시 alert창 생김


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
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')

        if password != check_pswd:
            return render(request, 'SignUp/alert.html')
            # 비밀번호가 같지않으면 alert
        else:
            exist_user = User.objects.filter(email=email)
            if (exist_user == None):
                return render(request, 'SignUp/alert3.html')
                # 존재하는 아이디면 alert
            else:
                user = get_user_model().objects.create_user(email, username, password)

                user.birthday_year = birthday_year
                user.birthday_month = birthday_month
                user.birthday_date = birthday_date
                user.gender = gender
                user.email = email
                user.mobile = mobile
                user.name = name

                user.save()

                return redirect('/user/login/')


@login_required
def Logout(request):
    logout(request)
    return redirect('/')


@login_required
def mypage(request):
    return render(request, 'logout/index.html')
