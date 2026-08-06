from base.views.base_view_set import BaseViewSet


class CompanyBaseViewSet(BaseViewSet):
    """
    Base ViewSet for company-scoped models.

    Automatically:
    - Filters records by the logged-in user's company.
    - Assigns the logged-in user's company on create.
    """

    def get_company(self):
        return self.request.user.employee.company

    def get_queryset(self):
        return super().get_queryset().filter(company=self.get_company())

    def perform_create(self, serializer):
        serializer.save(company=self.get_company())
