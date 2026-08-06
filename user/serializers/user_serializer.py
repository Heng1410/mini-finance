from rest_framework import serializers

from base.serializers.base_serializer import BaseSerializer
from employee.models.employee import Employee
from user.models.user import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_null=False, allow_blank=False)
    password = serializers.CharField(write_only=True, allow_blank=False)
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    class Meta:
        model = User
        fields = ("id", "username","password","employee")
        
    def create(self,validated_data):
        password = validated_data.pop("password")
        
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        
        return user
        
    def validate_employee(self, employee):
        if hasattr(employee, "user"):
            raise serializers.ValidationError(
                "This employee already has a user account."
            )
                
        return employee