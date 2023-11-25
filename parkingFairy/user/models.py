from django.db import models


class UserModel(models.Model):
    class Meta:  # DB Model 정보가 담긴 공간
        db_table = "my_user"

    username = models.CharField(max_length=20, null=False)
    password = models.CharField(max_length=256, null=False)
    email = models.CharField(max_length=30, null=False)
    birthday_year = models.CharField(max_length=4, null=False)
    birthday_month = models.CharField(max_length=2, null=False)
    birthday_date = models.CharField(max_length=2, null=False)
    gender = models.CharField(max_length=5, null=False)
    check_email = models.EmailField(max_length=30, null=False)
    mobile = models.CharField(max_length=16, null=False)
