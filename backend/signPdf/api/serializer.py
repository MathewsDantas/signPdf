from signPdf.models import Client
from rest_framework import serializers

class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('client_id','username', 'email', 'password')