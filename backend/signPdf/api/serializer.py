from signPdf.models import Client, Document
from rest_framework import serializers
from cryptography.fernet import Fernet

class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('client_id','username', 'email', 'password')

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('document_id', 'client', 'document_title', 'document_body', 'document_signature')
    
    key = 'hOujKhh4XzJayE2TU4sRXsp1tHhblWsCpC4o0V14U38='

    def encrypt_data(self, data):
        cipher_suite = Fernet(self.key)
        encrypted_data = cipher_suite.encrypt(data.encode('utf-8'))
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        cipher_suite = Fernet(self.key)
        decrypted_data = cipher_suite.decrypt(encrypted_data).decode('utf-8')
        return decrypted_data

    def to_internal_value(self, data):
        # Criar uma cópia mutável dos dados
        mutable_data = data.copy()

        # Criptografar os dados antes de criar a instância do modelo
        title_encrypted = self.encrypt_data(mutable_data.get('document_title', ''))
        body_encrypted = self.encrypt_data(mutable_data.get('document_body', ''))
        signature_encrypted = self.encrypt_data(mutable_data.get('document_signature', ''))

        # Atualizar a cópia mutável com os dados criptografados
        mutable_data['document_title'] = title_encrypted
        mutable_data['document_body'] = body_encrypted
        mutable_data['document_signature'] = signature_encrypted

        return super().to_internal_value(mutable_data)

    def to_representation(self, instance):
        # Descriptografa os dados antes de serializar
        title = self.decrypt_data(instance.document_title)
        body = self.decrypt_data(instance.document_body)
        signature = self.decrypt_data(instance.document_signature)

        representation = super().to_representation(instance)
        representation['document_title'] = title
        representation['document_body'] = body
        representation['document_signature'] = signature

        return representation

