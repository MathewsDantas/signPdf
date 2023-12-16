from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()

key = os.environ.get('FERNET_KEY')

def encrypt_data(data):
        cipher_suite = Fernet(key)
        encrypted_data = cipher_suite.encrypt(data.encode('utf-8'))
        return encrypted_data

def decrypt_data(encrypted_data):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode('utf-8')
    return decrypted_data
