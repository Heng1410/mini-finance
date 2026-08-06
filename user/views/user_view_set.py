from base.views.base_view_set import BaseViewSet
from user.models.user import User
from user.serializers.user_serializer import UserSerializer


class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    ordering = ["-date_joined"]

    def get_queryset(self):
        return self.queryset.select_related("employee")
