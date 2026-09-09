from rest_framework import serializers


class AttendanceSummarySerializer(serializers.Serializer):
    employee = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    total_days = serializers.IntegerField()
    present_days = serializers.IntegerField()
    late_days = serializers.IntegerField()
    half_days = serializers.IntegerField()
    absent_days = serializers.IntegerField()
    leave_days = serializers.IntegerField()
    
class AttendanceSummaryQuerySerializer(serializers.Serializer):
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)

    def validate(self, attrs):
        if attrs["start_date"] > attrs["end_date"]:
            raise serializers.ValidationError(
                "start_date must be before or equal to end_date."
            )
        return attrs