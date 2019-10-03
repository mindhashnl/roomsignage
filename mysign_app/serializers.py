from rest_framework import serializers

from mysign_app.models import Company, DoorDevice, User


class CompanySerializer(serializers.ModelSerializer):
    # email = serializers.EmailField()
    class Meta:
        model = Company
        fields = ['name', 'email', 'phone_number', 'id']


class DoorDeviceSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = DoorDevice
        fields = ['id', 'company']


class UserSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'company', 'is_admin']
