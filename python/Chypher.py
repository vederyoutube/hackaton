from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os

def encrypt(plaintext, key):
    backend = default_backend()

    # Генерация случайного IV (Initialization Vector)
    iv = os.urandom(16)

    RawKey = padding.PKCS7(128).padder()
    Key_data = RawKey.update(key.encode()) + RawKey.finalize()

    cipher = Cipher(algorithms.AES(Key_data), modes.CFB(iv), backend=backend)
    encryptor = cipher.encryptor()

    # Добавление дополнения для обработки текстов с переменной длиной
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()

    # Шифрование данных
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Кодирование IV и шифртекста в URL-безопасной Base64
    encrypted_message = urlsafe_b64encode(iv + ciphertext)

    return encrypted_message

def decrypt(encrypted_message, key):
    backend = default_backend()

    # Декодирование URL-безопасной Base64
    encrypted_message = urlsafe_b64decode(encrypted_message)

    # Извлечение IV из зашифрованных данных
    iv = encrypted_message[:16]
    ciphertext = encrypted_message[16:]

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)
    decryptor = cipher.decryptor()

    # Расшифрование данных
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Удаление дополнения
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_data) + unpadder.finalize()

    return plaintext.decode()