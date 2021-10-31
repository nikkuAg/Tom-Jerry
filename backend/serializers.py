from rest_framework import serializers
from .models import Address, User, Request_Confirm, Request_Sent, Audit
from .encryption_util import *


class UserSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        return {
            'id': obj.id,
            'username': decrypt(obj.username),
            'email': (obj.email),
            'phone': (obj.phone),
            'lastModified': obj.lastModified,
            'name': decrypt(obj.name),
            'aadhar': decrypt(obj.address.aadhar),
            'address': {
                'country': decrypt(obj.address.country),
                'district': decrypt(obj.address.district),
                'landmark': decrypt(obj.address.landmark),
                'house': decrypt(obj.address.house),
                'loc': decrypt(obj.address.loc),
                'pc': decrypt(obj.address.pc),
                'po': decrypt(obj.address.po),
                'state': decrypt(obj.address.state),
                'street': decrypt(obj.address.street),
                'subdistrict': decrypt(obj.address.subdistrict),
                'vtc':  decrypt(obj.address.vtc)
            }
        }

    class Meta:
        model = User
        fields = ['id', 'username', 'name',
                  'email', 'phone', 'lastModified', 'address']
        depth = 1


class AuditSerializer(serializers.ModelSerializer):
    client_pk = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='client'
    )
    introducer_pk = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='introducer'
    )

    class Meta:
        model = Audit
        fields = '__all__'
        depth = 1


class ConfirmSerializer(serializers.ModelSerializer):
    client_pk = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='client'
    )
    address_pk = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(), source='address'
    )

    class Meta:
        model = Request_Confirm
        fields = '__all__'
        depth = 1


class PasswordSearilizer(serializers.ModelSerializer):
    def to_representation(self, obj):
        return {
            'aadhar': decrypt(obj.introducer.address.aadhar),
            'country': decrypt(obj.introducer.address.country),
            'district': decrypt(obj.introducer.address.district),
            'landmark': decrypt(obj.introducer.address.landmark),
            'house': decrypt(obj.introducer.address.house),
            'loc': decrypt(obj.introducer.address.loc),
            'pc': decrypt(obj.introducer.address.pc),
            'po': decrypt(obj.introducer.address.po),
            'state': decrypt(obj.introducer.address.state),
            'street': decrypt(obj.introducer.address.street),
            'subdistrict': decrypt(obj.introducer.address.subdistrict),
            'vtc':  decrypt(obj.introducer.address.vtc)
        }

    class Meta:
        model = Request_Confirm
        fields = ['introducer']
        depth = 2


class SentSerializer(serializers.ModelSerializer):

    introducer_pk = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='introducer'
    )

    class Meta:
        model = Request_Sent
        fields = '__all__'
        depth = 1


class ClientSentSerializer(serializers.ModelSerializer):
    request_client = SentSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['request_client']

    # phone number and email
