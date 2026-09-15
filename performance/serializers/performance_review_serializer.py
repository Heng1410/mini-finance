from rest_framework import serializers

from performance.models.performance_review import PerformanceReview

 
class PerformanceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceReview
        fields = [
            "id",
            "employee",
            "reviewer",
            "review_period_start",
            "review_period_end",
            "rating",
            "comments",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "reviewer",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        if attrs["review_period_end"] < attrs["review_period_start"]:
            raise serializers.ValidationError(
                {
                    "review_period_end": (
                        "Review period end must be later than or equal to "
                        "review period start."
                    )
                }
            )

        if not 1 <= attrs["rating"] <= 5:
            raise serializers.ValidationError(
                {
                    "rating": "Rating must be between 1 and 5."
                }
            )

        return attrs


class PerformanceReviewListSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    reviewer_name = serializers.SerializerMethodField()

    class Meta:
        model = PerformanceReview
        fields = [
            "id",
            "employee",
            "employee_name",
            "reviewer",
            "reviewer_name",
            "review_period_start",
            "review_period_end",
            "rating",
            "status",
        ]

    def get_employee_name(self, obj):
        return f"{obj.employee.first_name} {obj.employee.last_name}"

    def get_reviewer_name(self, obj):
        return f"{obj.reviewer.first_name} {obj.reviewer.last_name}"


class PerformanceReviewDetailSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    reviewer_name = serializers.SerializerMethodField()

    class Meta:
        model = PerformanceReview
        fields = [
            "id",
            "employee",
            "employee_name",
            "reviewer",
            "reviewer_name",
            "review_period_start",
            "review_period_end",
            "rating",
            "comments",
            "status",
            "created_at",
            "updated_at",
        ]

    def get_employee_name(self, obj):
        return f"{obj.employee.first_name} {obj.employee.last_name}"

    def get_reviewer_name(self, obj):
        return f"{obj.reviewer.first_name} {obj.reviewer.last_name}"