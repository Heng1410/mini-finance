from datetime import timedelta

from django.db import transaction

from case_support.constants import CasePriority
from case_support.models.case import Case
from case_support.models.case_sla import CaseSla


class CaseSlaService:

    SLA_RULES = {
        CasePriority.CRITICAL: {
            "response": timedelta(minutes=15),
            "resolution": timedelta(hours=1),
        },
        CasePriority.HIGH: {
            "response": timedelta(minutes=30),
            "resolution": timedelta(hours=4),
        },
        CasePriority.MEDIUM: {
            "response": timedelta(hours=1),
            "resolution": timedelta(hours=8),
        },
        CasePriority.LOW: {
            "response": timedelta(hours=4),
            "resolution": timedelta(hours=24),
        },
    }

    @classmethod
    @transaction.atomic
    def create_sla(cls, *, company, case):
        case = Case.objects.get(
            pk=case.pk,
            company=company,
        )

        if hasattr(case, "sla"):
            return case.sla

        sla_rule = cls.SLA_RULES.get(case.priority)

        if not sla_rule:
            raise ValueError(f"No SLA rule configured for priority: {case.priority}")

        start_time = case.created_at

        response_due_at = start_time + sla_rule["response"]
        resolution_due_at = start_time + sla_rule["resolution"]

        sla = CaseSla.objects.create(
            company=company,
            case=case,
            response_due_at=response_due_at,
            resolution_due_at=resolution_due_at,
        )

        return sla
