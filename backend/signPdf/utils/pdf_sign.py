import uuid
from io import BytesIO
from pyhanko import stamp
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import fields, signers

from signPdf.models import Document

class PDFSigner:
    def __init__(self, document, pdf):
        self.pdf = pdf
        self.hash = document.document_hash
        self.key_pem_path = "./signPdf/utils/keys/private_key.pem"
        self.cert_pem_path = "./signPdf/utils/keys/cert_key.pem"

    def sign(self):
        # Carrega o certificado e a chave privada do caminho fornecido
        signer = signers.SimpleSigner.load(
            self.key_pem_path, self.cert_pem_path, ca_chain_files=(), key_passphrase=None
        )
        print('SIGNER: ',signer)
        # Cria um escritor incremental para o arquivo PDF a ser assinado
        w = IncrementalPdfFileWriter(BytesIO(self.pdf))

        # Adiciona um campo de assinatura ao PDF
        fields.append_signature_field(w, sig_field_spec=fields.SigFieldSpec("Signature", box=(100, 100, 500, 160)))

        # Configura metadados para a assinatura
        meta = signers.PdfSignatureMetadata(field_name="Signature")

        # Configura o PDFSigner com o carimbo e outros detalhes da assinatura
        pdf_signer = signers.PdfSigner(
            meta,
            signer=signer,
            stamp_style=stamp.QRStampStyle(
                stamp_text="Assinado por: %(signer)s\nData: %(ts)s\nURL: %(url)s",
            ),
        )

        # Cria um buffer de bytes para armazenar o PDF assinado
        out = BytesIO()

        # # Realiza a assinatura do PDF
        pdf_signer.sign_pdf(
            w, output=out, appearance_text_params={"url": f"http://localhost:8000/api/v1/pdf/get_by_hash/?hash={self.hash}"},
        )

        # Retorna o PDF assinado e o identificador único
        return out
