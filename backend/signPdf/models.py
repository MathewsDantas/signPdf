from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from signPdf.managers import UsuarioManager
from simple_history.models import HistoricalRecords
from safedelete.models import SafeDeleteModel


class Client(SafeDeleteModel, AbstractUser):
    username = models.CharField(
        max_length=200, unique=True, validators=[AbstractUser.username_validator]
    )
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    history = HistoricalRecords()
    objects = UsuarioManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    groups = models.ManyToManyField(Group, related_name="cliente", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="clientes", blank=True
    )

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f"{self.username} - {self.email}"


class Document(SafeDeleteModel):
    document_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    document_title = models.CharField(max_length=200)
    document_body = models.CharField(max_length=500)
    document_signature = models.CharField(max_length=200)
    document_hash = models.CharField(max_length=500, blank=True, null=True)
    signature_date = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"

    def __str__(self):
        return f"{self.document_id} - {self.document_title}"
