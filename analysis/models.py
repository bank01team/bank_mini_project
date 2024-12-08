from django.db import models

from bank.models import Accounts
from member.models import Users


# Create your models here.
class Analysis(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    about = models.CharField(max_length=50, verbose_name="About")
    type = models.CharField(max_length=50, verbose_name="Type")
    period_start = models.DateField(verbose_name="Start Date")
    period_end = models.DateField(verbose_name="End Date")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    result_image = models.ImageField(null=True, upload_to="analysis/image", verbose_name="Result Image")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
