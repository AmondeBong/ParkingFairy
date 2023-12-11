
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, username, password, **extra_fields):

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):

        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )

        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    objects = UserManager()

    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        max_length=20,
        null=False,
        unique=True
    )

    birthday_year = models.CharField(max_length=4, null=True)
    birthday_month = models.CharField(max_length=2, null=True)
    birthday_date = models.CharField(max_length=2, null=True)
    gender = models.CharField(max_length=5, null=True)
    mobile = models.CharField(max_length=12, null=True, default='01000000000')
    car = models.JSONField('json', null=True, default=dict)
    name = models.CharField(max_length=30, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:  # DB Model 정보가 담긴 공간
        db_table = "my_user"
