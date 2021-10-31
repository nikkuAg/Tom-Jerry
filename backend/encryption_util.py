from cryptography.fernet import Fernet
import base64
import logging
import traceback
from UIDAI.config import ENCRYPT_KEY


def encrypt(txt):
    try:
        print("Encrypt")
        txt = str(txt)
        cipher_suite = Fernet(ENCRYPT_KEY)  # key should be byte
        encrypted_text = cipher_suite.encrypt(txt.encode('ascii'))
        encrypted_text = base64.urlsafe_b64encode(
            encrypted_text).decode("ascii")
        return encrypted_text
    except Exception as e:
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


def decrypt(txt):
    try:
        print("Decrypt")
        txt = base64.urlsafe_b64decode(txt)
        cipher_suite = Fernet(ENCRYPT_KEY)
        decoded_text = cipher_suite.decrypt(txt).decode("ascii")
        print("Decrypt", decoded_text)
        return decoded_text
    except Exception as e:
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None
