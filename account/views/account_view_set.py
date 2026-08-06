from rest_framework.decorators import action
from rest_framework.response import Response

from account.models.account import Account
from account.serializers.account_serializer import (
    AccountDetailSerializer,
    AccountListSerializer,
    AccountSerializer,
)
from base.views.company_base_view_set import CompanyBaseViewSet
from account.serializers.account_tree_serializer import AccountTreeSerializer


class AccountViewSet(CompanyBaseViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        queryset = super().get_queryset().select_related("parent")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return AccountListSerializer

        if self.action == "retrieve":
            return AccountDetailSerializer

        if self.action == "tree":
            return AccountTreeSerializer

        return AccountSerializer

    @action(detail=False, methods=["get"])
    def tree(self, request):
        queryset = (
            self.get_queryset().filter(parent__isnull=True).prefetch_related("children")
        )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
