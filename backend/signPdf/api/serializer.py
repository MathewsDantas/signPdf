from signPdf.models import Client, Document
from rest_framework import serializers
from signPdf.utils.cryptograpy import encrypt_data, decrypt_data

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import hashlib

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id','username', 'email', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        
        client = Client(**validated_data)

        if password:
            client.set_password(password)

        client.save()
        
        return client

class DocumentSerializer(serializers.ModelSerializer):
    client = serializers.CharField(read_only=True)
    document_hash = serializers.CharField(read_only=True)

    class Meta:
        model = Document
        fields = ('document_id', 'client', 'document_title', 'document_body', 'document_signature', 'document_hash')
    
    def create(self, data):
        # Criar uma cópia mutável dos dados
        mutable_data = data.copy()
        # Calcula o hash antes da criptografia
        data_to_hash = f"{mutable_data.get('document_title', '')}{mutable_data.get('document_body', '')}"
        hash_value = hashlib.sha256(data_to_hash.encode()).hexdigest()

        # Atualizar a cópia mutável com o hash calculado
        mutable_data['document_hash'] = hash_value

        # Criptografar os dados antes de criar a instância do modelo
        title_encrypted = encrypt_data(mutable_data.get('document_title', ''))
        body_encrypted = encrypt_data(mutable_data.get('document_body', ''))
        signature_encrypted = encrypt_data(mutable_data.get('document_signature', ''))
        # Atualizar a cópia mutável com os dados criptografados
        mutable_data['document_title'] = title_encrypted.decode('utf-8')
        mutable_data['document_body'] = body_encrypted.decode('utf-8')
        mutable_data['document_signature'] = signature_encrypted.decode('utf-8')
        client = self.context['request'].user
        mutable_data['client'] = client

        return super().create(mutable_data)

    def to_representation(self, instance):
        # Descriptografa os dados antes de serializar
        title = decrypt_data(instance.document_title)
        body = decrypt_data(instance.document_body)
        signature = decrypt_data(instance.document_signature)

        representation = super().to_representation(instance)
        representation['document_title'] = title
        representation['document_body'] = body
        representation['document_signature'] = signature

        return representation
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["nome"] = user.username
        token["email"] = user.email

        return token

