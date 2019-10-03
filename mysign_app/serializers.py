from rest_framework import routers, serializers, viewsets

from mysign_app.models import DoorDevice, Company, User


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
