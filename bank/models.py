from django.db import models

from member.models import Users


# Create your models here.
class Accounts(models.Model):
    account_number = models.CharField(max_length=50, unique=True)
    bank_code = models.CharField(max_length=10)
    balance = models.IntegerField()
    account_type = models.CharField(max_length=20)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)


class DepositWithdraw(models.Model):
    class DepositWithdrawType(models.TextChoices):
        DEPOSIT = "입금", "입금"  # (데이터베이스 값, 표시 레이블)
        WITHDRAW = "출금", "출금"


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        CASH = "현금", "현금"
        TRANSFER = "계좌이체", "계좌이체"
        AUTO_TRANSFER = "자동이체", "자동이체"
        CARD = "카드결제", "카드결제"


class TransactionHistory(models.Model):
    deposit = models.IntegerField()
    withdraw = models.IntegerField()
    balance = models.IntegerField(null=True, blank=True)
    details = models.CharField(max_length=50)
    dw_type = models.CharField(max_length=10, choices=DepositWithdraw.DepositWithdrawType)
    ts_type = models.CharField(max_length=10, choices=Transaction.TransactionType)
    td_date = models.DateField(auto_now_add=True)
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
