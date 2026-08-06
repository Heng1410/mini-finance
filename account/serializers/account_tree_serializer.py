from rest_framework import serializers

from account.models.account import Account
from base.serializers.base_serializer import BaseSerializer


class AccountTreeSerializer(BaseSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ("id", "code", "name", "account_type", "children")

    def get_children(self, obj):
        children = obj.children.all().order_by("code")
        return AccountTreeSerializer(children, many=True).data
