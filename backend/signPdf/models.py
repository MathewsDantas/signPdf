from django.db import models
from django.contrib.auth.models import User

class Client(User):
    client_id = models.AutoField(primary_key=True)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return self.username
    
class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    document_title = models.CharField(max_length=200)
    document_body = models.CharField(max_length=500)
    document_signature = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return self.document_name