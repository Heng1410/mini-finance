from django.db import models


class StockReserveStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    CONFIRMED = "CONFIRMED", "Confirmed"
    RELEASED = "RELEASED", "Released"
    EXPIRED = "EXPIRED", "Expired"


class StockMovementType(models.TextChoices):
    PURCHASE = "PURCHASE", "Purchase"
    SALE = "SALE", "Sale"
    DAMAGE = "DAMAGE", "Damage"
    ADJUSTMENT_IN = "ADJUSTMENT_IN", "Adjustment_in"
    ADJUSTMENT_OUT = "ADJUSTMENT_OUT", "Adjustment_out"
    INITIAL = "INITIAL", "Initial"
