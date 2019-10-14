from rest_framework import serializers

from mysign_app.models import Company, DoorDevice, User


class CompanySerializer(serializers.ModelSerializer):
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
    name = serializers.SerializerMethodField('get_full_name')

    def get_full_name(self, obj):
        return obj.get_full_name()

    class Meta:
        model = User
        fields = ['id', 'name', 'first_name', 'last_name', 'email', 'company', 'is_admin']
