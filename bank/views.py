from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from bank.models import Accounts, TransactionHistory
from bank.serializers import BankTransactionSerializer


# Create your views here.
class TransactionHistoryView(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet[TransactionHistory]):
    queryset = TransactionHistory.objects.all()
    serializer_class = BankTransactionSerializer
    lookup_field = "id"

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
        dw_type = request.query_params.get("dw_type")

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
