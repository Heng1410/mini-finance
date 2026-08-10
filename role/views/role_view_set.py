from base.views.base_view_set import BaseViewSet
from role.models.role import Role
from role.serializers.role_serializer import (
    RoleDetailSerializer,
    RoleListSerializer,
    RoleSerializer,
)


class RoleViewSet(BaseViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = self.queryset.select_related("company")

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return RoleListSerializer

        if self.action == "retrieve":
            return RoleDetailSerializer

        return RoleSerializer
