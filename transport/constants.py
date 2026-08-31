from django.db import models


class VehicleType(models.TextChoices):
    CAR = "CAR", "Car"
    MOTORCYCLE = "MOTORCYCLE", "Motorcycle"
    TRUCK = "TRUCK", "Truck"
    VAN = "VAN", "Van"


class VehicleStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    MAINTENANCE = "MAINTENANCE", "Maintenance"
    
class MaintenanceType(models.TextChoices):
    OIL_CHANGE = "OIL_CHANGE", "Oil Change"
    REPAIR = "REPAIR", "Repair"
    SERVICE = "SERVICE", "Service"
    TIRE_CHANGE = "TIRE_CHANGE", "Tire Change"
    INSPECTION = "INSPECTION", "Inspection"
    
class TransportType(models.TextChoices):
    DELIVERY = "DELIVERY", "Delivery"
    PICKUP = "PICKUP", "Pickup"
    PASSENGER = "PASSENGER", "Passenger"
    TRANSFER = "TRANSFER", "Transfer"
    OTHER = "OTHER", "Other"


class TransportStatus(models.TextChoices):
    PLANNED = "PLANNED", "Planned"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"
    
class TransportExpenseType(models.TextChoices):
    FUEL = "FUEL", "Fuel"
    TOLL = "TOLL", "Toll"
    PARKING = "PARKING", "Parking"
    MAINTENANCE = "MAINTENANCE", "Maintenance"
    DRIVER_ALLOWANCE = "DRIVER_ALLOWANCE", "Driver Allowance"
    OTHER = "OTHER", "Other"
    
class FuelType(models.TextChoices):
    PETROL = "PETROL", "Petrol"
    DIESEL = "DIESEL", "Diesel"
    ELECTRIC = "ELECTRIC", "Electric"
    HYBRID = "HYBRID", "Hybrid"
    LPG = "LPG", "LPG"
    OTHER = "OTHER", "Other"
    
class BookingStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"