from random import randrange, getrandbits
import hashlib
from Crypto.PublicKey import RSA
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.x509.oid import NameOID
from cryptography import x509
import datetime
import os
import os.path
from pathlib import PurePath, Path

class Cryp:
    def __init__(self):
        pass
    def generate_RSA_pair(self, bit_length):
        key = RSA.generate(bit_length)
        Path('private.pem').touch()
        f = open("private.pem", "wb")
        f.write(key.export_key()) # private key

        pubKey = key.publickey()
        Path('public.pem').touch()
        f = open("public.pem", "wb")
        f.write(pubKey.export_key()) # private key

    def import_pem_key_file(self, f):
        with open(f,'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password = None,
                backend = default_backend()
            )
            if f == "private.pem":
                return private_key
            else:
                public_key = private_key.public_key()
                return public_key

    def generate_crypt_resume(self, doc):
        out = hashlib.sha256(doc.encode()).hexdigest()
        return out

class ACRoot:

    def gera_cert(self, subject):
        vetor = subject.split()
        # defino atributos do certificado gerado
        issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"BR"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"SC"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "AC_root"),
        ])
        subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, vetor[0]),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, vetor[1]),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, vetor[2]),
        ])
        # buildo o certifiicado
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            self.private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            # valido p 10 dias
            datetime.datetime.utcnow() + datetime.timedelta(days=10)
        ).add_extension(
            x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
            critical = False,
        # assino certificado
        ).sign(self.private_key, hashes.SHA256(), default_backend())

        # defino o nome do arquivo para seu numero serial
        string = os.getcwd() + "/certificados/" + str(cert.serial_number)+".pem"
        #  pathlib import feito para generalizar independente do SO
        a = PurePath(string)
        a = str(a)

        if not os.path.exists('certificados'):
            os.makedirs('certificados')

        open(a, 'a').close()
        with open(a, "wb") as f:
            # metodo para gerar arquivo PEM
            f.write(cert.public_bytes(serialization.Encoding.PEM))


    def __init__(self, private_key): # , certificado_storage
        self.private_key = private_key
        # deve criar e auto assinar seu certificado:
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"BR"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Santa Catarina"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"UFSC"),
        ])
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            self.private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            # valido p 10 dias
            datetime.datetime.utcnow() + datetime.timedelta(days=10)
        ).add_extension(
            x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
            critical = False,
        ).sign(self.private_key, hashes.SHA256(), default_backend())
        # escreve no disco
        with open("AC_certificate.pem", "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))

        # defino o certificado como a variavel global "certificado" da AC
        self.certificado = cert
def get_cert(file):
    f = open(file, 'rb')
    data = f.read()

    out = x509.load_pem_x509_certificate(data, default_backend())
    return out

def get_cert_info(cert):
    out = [cert.subject.rfc4514_string(), str(cert.serial_number), cert.issuer.rfc4514_string()]
    return out

     # def store_cert():
def list_certificates(var): # var = 1, listar por subject var = 2 listar por serial
    AC = ACRoot
    out = []
    file = PurePath(os.getcwd(), 'certificados')
    for filename in os.listdir(file):
        vet = filename.split(".")
        file = PurePath('certificados', filename)
        file = str(file)
        if var == 1:
            subject_str = get_cert(file).subject.rfc4514_string()
            out.append(subject_str)
        else:
            out.append(vet[0])
    return out
