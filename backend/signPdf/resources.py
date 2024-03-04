from import_export.resources import ModelResource
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from .models import Client, Document


class ClientResource(ModelResource):
    class Meta:
        model = Client
        export_order = ("id", "username", "email", "password")
        fields = export_order  # serve para exportar apenas os campos que estão na lista
        import_id_fields = ("username",)
        skip_unchanged = True


class DocumentResource(ModelResource):
    client = Field(
        column_name="client",
        attribute="client",
        widget=ForeignKeyWidget(Client, "username"),
    )

    class Meta:
        model = Document
        export_order = (
            "document_id",
            "client",
            "document_title",
            "document_body",
            "document_signature",
            "document_hash",
        )
        fields = export_order  # serve para exportar apenas os campos que estão na lista
        import_id_fields = ("document_title",)
        skip_unchanged = True
