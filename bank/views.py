from typing import Any

from django.db import transaction
from django.db.models import QuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from bank.models import Accounts, TransactionHistory
from bank.serializers import BankTransactionSerializer

from .models import Accounts
from .serializers import AccountSerializer


# Create your views here.
class TransactionHistoryView(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet[TransactionHistory]):
    permission_classes = [IsAuthenticated]
    queryset = TransactionHistory.objects.all().prefetch_related()
    serializer_class = BankTransactionSerializer
    lookup_field = "id"

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        account = Accounts.objects.get(user_id=request.user.id, id=request.data["account"])
        balance = account.balance
        if request.data["dw_type"] == "입금":
            account.balance = request.data["deposit"] + balance
            request.data["balance"] = account.balance
            serializer = self.get_serializer(data=request.data)
        else:
            account.balance = balance - request.data["withdraw"]
            request.data["balance"] = account.balance
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            serializer.save()
            account.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(  # type: ignore
        manual_parameters=[
            openapi.Parameter(
                "ts_type", openapi.IN_QUERY, description="현금,계좌이체,자동이체,카드결제", type=openapi.TYPE_STRING
            ),
            openapi.Parameter("dw_type", openapi.IN_QUERY, description="입금,출금", type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request: Request):
        ts_type = request.query_params.get("ts_type")
        dw_type = request.query_params.get("w_type")

        accounts = Accounts.objects.filter(user_id=request.user.id)
        response = {}
        for account in accounts:
            transactions = account.transactionhistory_set.all()
            if ts_type:
                transactions = transactions.filter(ts_type=ts_type)
            if dw_type:
                transactions = transactions.filter(dw_type=dw_type)
            response[account.account_number] = BankTransactionSerializer(transactions, many=True).data

        return Response(response)

    def update(self, request: Request, **kwargs: dict[str, bool]) -> Response:
        transaction = TransactionHistory.objects.get(id=self.kwargs[self.lookup_field])
        account = Accounts.objects.get(id=transaction.account_id)
        if account.user_id != request.user.id:
            raise PermissionDenied()
        return super().update(request, **kwargs)

    def destroy(self, request: Request) -> Response:
        transaction = TransactionHistory.objects.get(id=self.kwargs[self.lookup_field])
        account = Accounts.objects.get(id=transaction.account_id)
        if account.user_id != request.user.id:
            raise PermissionDenied()
        return super().destroy(request)


class AccountViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet[Accounts]):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer
    queryset = Accounts.objects.all()

    def list(self, request: Request) -> Response:

        user_id = request.user.id
        account_list = Accounts.objects.filter(user_id=user_id)
        serializer = AccountSerializer(account_list, many=True)

        return Response(serializer.data)
