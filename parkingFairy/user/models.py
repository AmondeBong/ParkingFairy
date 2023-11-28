from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, username, password, email, birthday_year, birthday_month, birthday_date, gender, check_email, mobile):
        user = self.model(
            username=username,
            email=email,
            birthday_year=birthday_year,
            birthday_month=birthday_month,
            birthday_date=birthday_date,
            gender=gender,
            check_email=check_email,
            mobile=mobile,
            password=password
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, id, email, password):

        user = self.model(
            check_email=email,
            email=id,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    objects = UserManager()

    email = models.CharField(max_length=25, verbose_name="ID", unique=True)
    password = models.CharField(max_length=256, verbose_name="PW")
    check_email = models.EmailField(
        max_length=128, verbose_name="email", null=True, unique=True)
    username = models.CharField(
        max_length=70, verbose_name="username", null=True)
    # auth = models.CharField(max_length=10, verbose_name="auth", null=True)
    date_joined = models.DateTimeField(
        auto_now_add=True, verbose_name='date_joined', null=True, blank=True)
    birthday_year = models.CharField(max_length=4, null=False)
    birthday_month = models.CharField(max_length=2, null=False)
    birthday_date = models.CharField(max_length=2, null=False)
    gender = models.CharField(max_length=5, null=False)
    mobile = models.CharField(max_length=16, null=False, default='01000000000')
    car = models.JSONField('json', default=dict)

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:  # DB Model 정보가 담긴 공간
        db_table = "my_user"
