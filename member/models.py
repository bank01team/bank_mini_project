from datetime import datetime
from typing import Any, Dict, Union

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.
class UserManager(BaseUserManager["Users"]):
    def create_user(self, email:str, name:str, password:str, **extra_fields:dict[str,Any])->"Users":
        if not email:
            raise ValueError("이메일은 필수입니다")
        if not name:
            raise ValueError("이름은 필수입니다")
        if not password:
            raise ValueError("비밀번호는 필수입니다")

        user = self.model(email=self.normalize_email(email), name=name, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email:str, name:str, password:str, **extra_fields:Any)->"Users":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_admin") is not True:
            raise ValueError("Superuser must have is_admin=True.")

        return self.create_user(email, name, password, **extra_fields)

class Users(AbstractBaseUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=50, null=True)
    nickname = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def has_perm(self, perm:Any, obj:Any=None)->bool:
        return True

    def has_module_perms(self, app_label:Any)->bool:
        return True

