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
from rest_framework.permissions import IsAuthenticated

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
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

            # Criar o objeto PDF usando o canvas do reportlab
            p = canvas.Canvas(response_data)
            
            # Adicionar informações ao PDF
            p.drawString(100, 800, f'Título do Documento: {decrypt_data(document.document_title)}')
            p.drawString(100, 780, f'Corpo do Documento: {decrypt_data(document.document_body)}')
            p.drawString(100, 760, f'Assinatura do Documento: {decrypt_data(document.document_signature)}')

            # Fechar o objeto PDF
            p.showPage()
            p.save()

            # Adicionar mensagem de sucesso
            success_message = {"message": "PDF gerado com sucesso."}
            response_data["success_message"] = success_message

            return response_data
        except Document.DoesNotExist:
            response_data = {"message": "Erro ao gerar o PDF, verifique o id do documento fornecido."}
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'], url_path='check-document-by-hash')
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'document_hash': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['hash'],
        ),
        responses={
            200: openapi.Response(description="Documento encontrado"),
            404: openapi.Response(description="Nenhum documento encontrado com o hash fornecido."),
        }
    )
    def check_document_by_hash(self, request):
        # Obter o valor do hash a partir do corpo da solicitação
        hash_value = request.data.get('document_hash', '')

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