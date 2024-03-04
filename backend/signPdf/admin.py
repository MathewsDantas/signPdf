from .base.admin import BaseModelAdmin
from django.contrib.admin import register, display
from .resources import ClientResource, DocumentResource
from django.utils.safestring import mark_safe

from .models import Client, Document


# Register your models here.
@register(Client)
class ClientAdmin(BaseModelAdmin):
    resource_class = ClientResource
    list_display = (
        "username",
        "email",
        "password",
        "is_active",
        "is_staff",
        "get_published_date",
    )
    search_fields = ("username", "email")
    list_filter = [
        "is_active",
    ] + BaseModelAdmin.list_filter
    list_editable = [
        "is_active",
    ]
    readonly_fields = [
        "password",
    ]
    date_hierarchy = "date_joined"
    fieldsets = [
        (("Identificação"), {"fields": ["username", "email"]}),
        (
            ("Mais infos"),
            {"fields": ["password", "is_active", "is_staff"]},
        ),
    ]

    def get_published_date(self, obj):
        return obj.date_joined.strftime("%d %b %Y %H:%M:%S")


@register(Document)
class DocumentAdmin(BaseModelAdmin):
    resource_class = DocumentResource
    list_display = (
        "client",
        "document_title",
        "document_body",
        "document_signature",
        "document_hash",
    )
    search_fields = (
        "client",
        "document_title",
        "document_body",
        "document_signature",
        "document_hash",
    )
    fieldsets = [
        (("Identificação"), {"fields": ["client"]}),
        (
            ("Mais infos"),
            {
                "fields": [
                    "document_title",
                    "document_body",
                    "document_signature",
                    "document_hash",
                ]
            },
        ),
    ]
