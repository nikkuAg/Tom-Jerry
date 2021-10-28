from rest_framework import serializers
from .models import User, Request_Confirm, Request_Sent, Audit


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'aadharNo',
                  'email', 'phone', 'lastModified']


class AuditSerializer(serializers.ModelSerializer):
    client_pk = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='client3', many=True
    )
    introducer_pk = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='interducer3', many=True
    )

    class Meta:
        model = Audit
        fields = '__all__'
        depth = 1


class ConfirmSerializer(serializers.ModelSerializer):
    client_pk = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='client2', many=True
    )
    introducer_pk = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='interducer2', many=True
    )

    class Meta:
        model = Request_Confirm
        fields = '__all__'
        depth = 1


class SentSerializer(serializers.ModelSerializer):
    client_pk = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='client1', many=True
    )
    introducer_pk = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='interducer1', many=True
    )

    class Meta:
        model = Request_Sent
        fields = '__all__'
        # depth = 1
