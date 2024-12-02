from django.db.models import QuerySet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import Accounts
from .serializers import AccountSerializer


class AccountViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet[Accounts]):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer
    queryset = Accounts.objects.all()

    def list(self, request: Request) -> Response:

        user_id = request.user.id
        account_list = Accounts.objects.filter(user_id=user_id)
        serializer = AccountSerializer(account_list, many=True)

        return Response(serializer.data)
