from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from base.views.company_base_view_set import CompanyBaseViewSet
from employee.models.employee import Employee
from performance.models.performance_review import PerformanceReview
from performance.serializers.performance_review_serializer import (
    PerformanceReviewDetailSerializer,
    PerformanceReviewListSerializer,
    PerformanceReviewSerializer,
)
from performance.services.performance_review_service import PerformanceReviewService


class PerformanceReviewViewSet(CompanyBaseViewSet):
    model = PerformanceReview

    queryset = PerformanceReview.objects.select_related("employee", "reviewer")

    serializer_class = PerformanceReviewSerializer

    filter_backends = CompanyBaseViewSet.filter_backends + (DjangoFilterBackend,)

    filterset_fields = {
        "employee": ["exact"],
        "reviewer": ["exact"],
        "review_period_start": ["exact", "gte", "lte"],
        "review_period_end": ["exact", "gte", "lte"],
        "rating": ["exact", "gte", "lte"],
        "status": ["exact"],
    }

    search_fields = [
        "employee__first_name",
        "employee__last_name",
        "reviewer__first_name",
        "reviewer__last_name",
        "comments",
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceReviewListSerializer

        if self.action == "retrieve":
            return PerformanceReviewDetailSerializer

        return PerformanceReviewSerializer

    def perform_create(self, serializer):
        reviewer = self.request.user.employee

        employee = Employee.objects.get(
            id=serializer.validated_data["employee"],
            company=reviewer.company,
        )
        review = PerformanceReviewService.create_review(
            employee=employee,
            reviewer=reviewer,
            review_period_start=serializer.validated_data["review_period_start"],
            review_period_end=serializer.validated_data["review_period_end"],
            rating=serializer.validated_data["rating"],
            comments=serializer.validated_data.get("comments", ""),
        )

        serializer.instance = review

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        review = self.get_object()

        review = PerformanceReviewService.submit(review)

        serializer = PerformanceReviewDetailSerializer(review)

        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def acknowledge(self, request, pk=None):
        review = self.get_object()

        review = PerformanceReviewService.acknowledge(review)

        serializer = PerformanceReviewDetailSerializer(review)

        return Response(serializer.data)
