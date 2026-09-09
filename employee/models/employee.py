from django.db import models

from base.models.base_model import BaseModel
from company.models.company import Company
from department.models.department import Department
from role.models.role import Role
from work_schedule.models.work_schedule import WorkSchedule


# Create your models here.
class Employee(BaseModel):
    company = models.ForeignKey(
        Company, on_delete=models.PROTECT, related_name="employees"
    )
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name="employees"
    )
    work_schedule = models.ForeignKey(
        WorkSchedule,
        on_delete=models.PROTECT,
        related_name="employees",
        null=True,
        blank=True,
    )
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="employees")
    manager = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="subordinates",
        null=True,
        blank=True,
    )
    employee_code = models.CharField(max_length=16)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField()
    phone = models.CharField(max_length=32)
    hire_date = models.DateField()
    job_title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "employees"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "employee_code"], name="uq_company_employee_code"
            ),
        ]
