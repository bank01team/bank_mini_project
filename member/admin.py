from typing import Any, Sequence

from django.contrib import admin
from django.db.models import Model
from requests import Request

from .models import Users

# Register your models here.


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin): # type: ignore
    def get_fields(self, request:Any, obj: Model | None=None)->Sequence[str | Sequence[str]]:
        fields = super().get_fields(request, obj)
        if not request.user.is_admin:
            # 일반 사용자는 is_admin 필드를 볼 수 없음
            fields = [f for f in fields if f != "is_admin"]
        return fields

    list_filter = ("is_active", "is_staff")
    search_fields = ["email", "nickname", "phone"]
