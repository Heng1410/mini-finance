from rest_framework import serializers

from accounts_receivable.serializers.simple_sales_invoice_serializer import (
    SimpleSalesInvoiceSerializer,
)
from base.serializers.base_serializer import BaseSerializer
from accounts_receivable.models.customer import Customer


class CustomerSerializer(BaseSerializer):
    class Meta:
        model = Customer
        fields = ("id", "code", "name", "phone", "email", "address", "is_active")

    def validate_code(self, value):
        return value.strip().upper()

    def validate(self, attrs):
        company = self.context["request"].user.employee.company

        queryset = Customer.objects.filter(company=company, code=attrs["code"])

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError({"code": "Customer code already exists"})
        return super().validate(attrs)


class CustomerListSerializer(BaseSerializer):
    class Meta:
        model = Customer
        fields = ("id", "code", "name", "phone", "email")


class CustomerDetailSerializer(BaseSerializer):
    invoices = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = (
            "id",
            "code",
            "name",
            "phone",
            "email",
            "address",
            "is_active",
            "invoices",
        )

    def get_invoices(self, obj):
        invoices = obj.sales_invoices.all()
        return SimpleSalesInvoiceSerializer(invoices, many=True).data
