from rest_framework import serializers
from complaintApp.models import UserMaster, ComplaintMaster
from rest_framework.authtoken.models import Token


class UserMasterSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserMaster
        fields = ['email', 'custom_password', 'role']


class ComplaintMasterSerializer(serializers.ModelSerializer):
    created_by_email = serializers.CharField(source='created_by.email', allow_null=True, read_only=True)
    updated_by_email = serializers.CharField(source='updated_by.email', allow_null=True, read_only=True)

    class Meta:
        model = ComplaintMaster
        fields = ['id', 'complaint', 'status', 'created_by', 'updated_by', 'created_by_email', 'updated_by_email']