from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime


class Certificate:
    def __init__(self, document):
        self.document = document

    def generate_certificate(self):
        # Gerar uma chave privada RSA
        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )

        # Obter a chave pública
        public_key = private_key.public_key()

        # Criar um objeto de sujeito para o certificado
        subject = x509.Name(
            [
                x509.NameAttribute(NameOID.COUNTRY_NAME, "BR"),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Alecrim"),
                x509.NameAttribute(NameOID.LOCALITY_NAME, "Natal"),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, "My Organization"),
                x509.NameAttribute(NameOID.COMMON_NAME, self.document.client.username),
            ]
        )

        # Configurar o certificado
        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(subject)
            .public_key(public_key)
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.now())
            .not_valid_after(datetime.datetime.now() + datetime.timedelta(days=365))
            .add_extension(
                x509.BasicConstraints(ca=True, path_length=None), critical=True
            )
            .sign(private_key, hashes.SHA256(), default_backend())
        )

        # Converta a chave privada, a chave pública e o certificado para strings PEM
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode("utf-8")

        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")

        cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM).decode(
            "utf-8"
        )

        with open("./signPdf/utils/keys/private_key.pem", "w") as f:
            f.write(private_key_pem)

        with open("./signPdf/utils/keys/public_key.pem", "w") as f:
            f.write(public_key_pem)

        with open("./signPdf/utils/keys/cert_key.pem", "w") as f:
            f.write(cert_pem)

        return private_key_pem, public_key_pem, cert_pem
