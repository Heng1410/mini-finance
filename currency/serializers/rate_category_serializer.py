from rest_framework import serializers

from base.serializers.base_serializer import BaseSerializer
from currency.models.rate_category import RateCategory


class RateCategorySerializer(BaseSerializer):
    class Meta:
        model = RateCategory
        fields = ["id", "code", "name", "description", "default", "is_nbc"]

    def validate_code(self, value):
        value = value.strip().upper()

        if not value:
            raise serializers.ValidationError("Rate category code cannot be empty.")

        return value

    def validate_name(self, value):
        return value.strip()

    def validate_description(self, value):
        return value.strip()

    def validate(self, attrs):
        company = self.context["request"].user.employee.company
        code = attrs.get("code")

        queryset = RateCategory.objects.filter(
            company=company,
            code=code,
        )

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                {
                    "code": (
                        "A rate category with this code already exists "
                        "for this company."
                    )
                }
            )

        if attrs.get("default", False):
            default_queryset = RateCategory.objects.filter(
                company=company, default=True
            )

            if self.instance:
                default_queryset = default_queryset.exclude(
                    pk=self.instance.pk,
                )

            if default_queryset.exists():
                raise serializers.ValidationError(
                    {
                        "default": (
                            "A default rate category already exists "
                            "for this company."
                        )
                    }
                )

        return attrs


class RateCategoryListSerializer(BaseSerializer):
    class Meta:
        model = RateCategory
        fields = ["id", "code", "name", "description", "default", "is_nbc"]


class RateCategoryDetailSerializer(RateCategorySerializer):
    pass
