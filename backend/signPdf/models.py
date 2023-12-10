from django.db import models
from django.contrib.auth.models import User

class Client(User):
    client_id = models.AutoField(primary_key=True)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return self.username