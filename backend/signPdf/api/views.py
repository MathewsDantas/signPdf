from io import BytesIO
from signPdf.utils.generate_certificate import Certificate
from signPdf.utils.pdf_sign import PDFSigner
from signPdf.models import Client, Document
from rest_framework import viewsets, status
from .serializer import ClientSerializer, DocumentSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import MyTokenObtainPairSerializer
from rest_framework.decorators import action
from signPdf.utils.cryptograpy import decrypt_data
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, dict) and data.get("success", None) is False:
            return super(CustomRenderer, self).render(data, accepted_media_type, renderer_context)

        response = {"data": data, "metadata": {}, "success": True, "errors": []}

        if data and "metadata" in data:
            response["metadata"] = data.pop("metadata")

        # Handling pagination
        if data and hasattr(data, "keys") and "results" in data.keys():
            response["data"] = data["results"]
            for key in data.keys():
                if key != "results":
                    response["metadata"][key] = data[key]

        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)


class PermissionsMixin:
    """
    A mixin that permits to define a permission class for each action.
    """
    permission_classes = None

    def get_permissions(self):
        permission_classes = self.permission_classes
        if isinstance(permission_classes, dict):
            if self.action in permission_classes:
                return [permission() for permission in permission_classes[self.action]]
            return [permission() for permission in permission_classes["default"]]
        return [permission() for permission in permission_classes]
    

class CustomModelViewSet(PermissionsMixin, viewsets.ModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`, `partial_update()`, `destroy()` and `list()` actions.
    """

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    renderer_classes = [CustomRenderer]


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class DocumentViewSet(CustomModelViewSet):
    permission_classes = {
        "default": [permissions.IsAuthenticated],
        "generatePdf": [permissions.IsAuthenticated],
        "check_document_by_hash": [permissions.AllowAny],
    }
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    @action(detail=True, methods=['get'], url_path='generate-pdf')
    @swagger_auto_schema(
        responses={
            200: openapi.Response(description="PDF gerado com sucesso."),
            404: openapi.Response(description="Erro ao gerar o PDF, verifique o id do documento fornecido."),
        }
    )
    def generatePdf(self, request, pk=None):
        try:
            # Obter o documento do banco de dados usando o ID
            document = Document.objects.get(pk=pk)

            # Criar um objeto HttpResponse com o cabeçalho de conteúdo apropriado para um PDF.
            response_data = HttpResponse(content_type='application/pdf')
            response_data['Content-Disposition'] = f'attachment; filename={decrypt_data(document.document_title)}.pdf' 

            buffer = BytesIO()

            # Criar o objeto PDF usando o canvas do reportlab
            p = canvas.Canvas(buffer)
            
            # Adicionar informações ao PDF
            p.drawString(100, 800, f'Título do Documento: {decrypt_data(document.document_title)}')
            p.drawString(100, 780, f'Corpo do Documento: {decrypt_data(document.document_body)}')

            # Fechar o objeto PDF
            p.showPage()
            p.save() 

            Certificate(document).generate_certificate()

            pdf_bytes = buffer.getvalue() # Obtém o valor do buffer
            signed_pdf = PDFSigner(document, pdf_bytes).sign() # Assina o PDF

            response_data["message"] = "PDF gerado com sucesso."
            response_data.content = signed_pdf.getvalue()

            return response_data
        except Document.DoesNotExist:
            response_data = {"message": "Erro ao gerar o PDF, verifique o id do documento fornecido."}
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'], url_path='check-document-by-hash')
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'document_hash', 
                openapi.IN_QUERY, 
                description="Hash do documento a ser verificado", 
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: openapi.Response(description="Documento encontrado"),
            404: openapi.Response(description="Nenhum documento encontrado com o hash fornecido."),
        }
    )
    def check_document_by_hash(self, request):
        # Obter o valor do hash a partir do corpo da solicitação
        hash_value = request.query_params.get('document_hash', '')

        # Verificar se existe algum documento com o hash fornecido
        try:
            document = Document.objects.get(document_hash=hash_value)
            response_data = {"message": f"O Hash fornecido é de um documento válido: {decrypt_data(document.document_title)}"}
            return Response(response_data, status=status.HTTP_200_OK)
        except Document.DoesNotExist:
            response_data = {"message": "O Hash fornecido não é de um documento válido"}
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
