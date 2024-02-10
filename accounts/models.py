from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    """
    유저 생성 매니저
    """
    def create_user(self, google_id, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        # 사용자 생성 로직
        user = self.model(google_id=google_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, google_id, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # 슈퍼유저 생성 로직
        return self.create_user(google_id, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    유저 모델
    """
    google_id = models.CharField(max_length=30, unique=True, null = True)
    nickname = models.CharField(max_length=100, null = True)
    language = models.CharField(max_length=10)
    USERNAME_FIELD = 'google_id'
    EMAIL_FIELD = 'google_id'
    REQUIRED_FIELDS = []

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.nickname:  # 닉네임이 비어있을 때만 설정
            self.nickname = f"{self.pk}번째 부"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nickname
