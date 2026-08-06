from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )
    password = serializers.CharField(
        allow_blank=False,
        write_only=True,
        style={"input_type": "password"},
    )