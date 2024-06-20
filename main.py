from datetime import datetime
from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(
    title="Сервис для шифрования и дешифрования текста."
)

alphabet = ",.:(_)-0123456789АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
EXITING_LOGINS = ["bob1997", "carl-stalker1337", "ivan_v_tanke"]


class EncryptMethod(Enum):
    caesar: "caesar"
    vigenere: "vigenere"


class Users(BaseModel):
    id: int
    login: str = Field(min_length=3, max_length=30)
    secret: str


class MethodsOfEncryption(BaseModel):
    method: EncryptMethod
    caption: str = Field(max_length=30)
    json_params: dict
    descriptions: str = Field(max_length=1000)


class Sessions(BaseModel):
    id: int
    user_id: int
    method_id: int
    data_in: datetime
    params: str
    data_out: datetime
    status: int
    created_at: datetime


fake_users = [
    {"id": 1, "login": "bob1997", "secret": "qwert123"},
    {"id": 2, "login": "carl-stalker1337", "secret": "1337csgo1337"},
    {"id": 3, "login": "ivan_v_tanke", "secret": "world_of_tanks"}
]


@app.get("/encrypt/caesar")
def encrypt_caesar_method(text_for_encrypt: str, number_of_shifts: int):
    text_for_encrypt_upper = text_for_encrypt.upper()
    encrypted_text = []
    alphabet_size = len(alphabet)

    for char in text_for_encrypt_upper:
        if char in alphabet:
            original_index = alphabet.index(char)
            new_index = (original_index + number_of_shifts) % alphabet_size
            encrypted_text.append(alphabet[new_index])
        else:
            encrypted_text.append(char)

    return ''.join(encrypted_text)


@app.get("/decrypt/caesar")
def decrypt_caesar_method(text_for_decrypt: str, number_of_shifts: int):
    text_for_decrypt_upper = text_for_decrypt.upper()
    decrypted_text = []
    alphabet_size = len(alphabet)

    for char in text_for_decrypt_upper:
        if char in alphabet:
            encrypted_index = alphabet.index(char)
            new_index = (encrypted_index - number_of_shifts) % alphabet_size
            decrypted_text.append(alphabet[new_index])
        else:
            decrypted_text.append(char)

    return ''.join(decrypted_text)


@app.get("/encrypt/vigenere")
def encrypt_vigenere_method(text_for_encrypt: str, keyword: str):
    text_for_encrypt_upper = text_for_encrypt.upper()
    keyword_upper = keyword.upper()
    encrypted_text = []
    alphabet_size = len(alphabet)
    keyword_len = len(keyword_upper)

    for i, char in enumerate(text_for_encrypt_upper):
        if char in alphabet:
            original_index = alphabet.index(char)
            key_char = keyword_upper[i % keyword_len]
            key_index = alphabet.index(key_char)
            new_index = (original_index + key_index) % alphabet_size
            encrypted_text.append(alphabet[new_index])
        else:
            encrypted_text.append(char)

    return ''.join(encrypted_text)


@app.get("/decrypt/vigenere")
def decrypt_vigenere_method(text_for_decrypt: str, keyword: str):
    text_for_decrypt_upper = text_for_decrypt.upper()
    keyword_upper = keyword.upper()
    decrypted_text = []
    alphabet_size = len(alphabet)
    keyword_len = len(keyword_upper)

    for i, char in enumerate(text_for_decrypt_upper):
        if char in alphabet:
            encrypted_index = alphabet.index(char)
            key_char = keyword_upper[i % keyword_len]
            key_index = alphabet.index(key_char)
            new_index = (encrypted_index - key_index) % alphabet_size
            decrypted_text.append(alphabet[new_index])
        else:
            decrypted_text.append(char)

    return ''.join(decrypted_text)

