from rest_framework import serializers

from account.models.account import Account
from base.serializers.base_serializer import BaseSerializer


class AccountSerializer(BaseSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Account
        fields = (
            "id",
            "code",
            "name",
            "account_type",
            "parent",
            "description",
            "is_active",
            "role",
        )

    def validate_code(self, code):
        company = self.context["request"].user.employee.company

        queryset = Account.objects.filter(
            company=company,
            code__iexact=code,
        )

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("Account code already exists.")

        return code

    def validate_parent(self, parent):
        if parent is None:
            return parent

        company = self.context["request"].user.employee.company

        if parent.company != company:
            raise serializers.ValidationError(
                "Parent account must belong to the current company."
            )

        if self.instance and parent.pk == self.instance.pk:
            raise serializers.ValidationError("An account cannot be its own parent.")

        return parent

    def validate(self, attrs):
        return attrs


class AccountLookupSerializer(BaseSerializer):
    class Meta:
        model = Account
        fields = ("id", "code", "name")


class AccountListSerializer(BaseSerializer):
    parent = AccountLookupSerializer(read_only=True)

    class Meta:
        model = Account
        fields = ("id", "code", "name", "account_type", "parent", "is_active", "role")


class AccountDetailSerializer(AccountSerializer):
    parent = AccountLookupSerializer(read_only=True)
    pass
