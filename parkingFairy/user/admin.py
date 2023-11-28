from django.contrib import admin
from .models import User

admin.site.register(User)  # Admin에 UserModel 추가
# Register your models here.
