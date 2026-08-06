from django.contrib.auth.models import AbstractUser

from django.db import models

from employee.models.employee import Employee


# Create your models here.
class User(AbstractUser):
    employee = models.OneToOneField(
        Employee, on_delete=models.PROTECT, related_name="user", null=True, blank=True
    )

    class Meta:
        db_table = "users"
