from signPdf.models import Client, Document
from rest_framework import viewsets
from .serializer import ClientSerializer, DocumentSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import MyTokenObtainPairSerializer
from rest_framework.decorators import action
from signPdf.utils.cryptograpy import decrypt_data
from django.http import HttpResponse
from reportlab.pdfgen import canvas

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    @action(detail=True, methods=['post'], url_path='generate-pdf')
    def generatePdf(self, request, pk=None):

        # Obter o documento do banco de dados usando o ID
        document = Document.objects.get(pk=pk)

        # Criar um objeto HttpResponse com o cabeçalho de conteúdo apropriado para um PDF.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename={decrypt_data(document.document_title)}.pdf'

        # Criar o objeto PDF usando o canvas do reportlab
        p = canvas.Canvas(response)
        
        # Adicionar informações ao PDF
        p.drawString(100, 800, f'Título do Documento: {decrypt_data(document.document_title)}')
        p.drawString(100, 780, f'Corpo do Documento: {decrypt_data(document.document_body)}')
        p.drawString(100, 760, f'Assinatura do Documento: {decrypt_data(document.document_signature)}')

        # Fechar o objeto PDF
        p.showPage()
        p.save()

        return response

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer