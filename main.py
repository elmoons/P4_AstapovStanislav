from datetime import datetime
from enum import Enum
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(
    title="Сервис для шифрования и дешифрования текста."
)

alphabet = ",.:(_)-0123456789АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
EXITING_LOGINS = ["bob1997", "carl-stalker1337", "ivan_v_tanke"]


class Users(BaseModel):
    id: int
    login: str = Field(min_length=3, max_length=30)
    secret: str


class MethodsOfEncryption(BaseModel):
    id: int
    caption: str = Field(max_length=30)
    json_params: dict
    descriptions: str = Field(max_length=1000)


class Sessions(BaseModel):
    id: int
    user_id: int
    method_id: MethodsOfEncryption
    data_in: datetime
    params: str
    data_out: str
    status: int
    created_at: datetime
    time_op: float


fake_users = [
    {"id": 1, "login": "bob1997", "secret": "qwert123"},
    {"id": 2, "login": "carl-stalker1337", "secret": "1337csgo1337"},
    {"id": 3, "login": "ivan_v_tanke", "secret": "world_of_tanks"}
]


methods_of_encryptions = [
    {"id": 1, "caption": "Method of Caesar", "json_params": {"text": "str", "shifts": "int"}, "descriptions": "The Caesar Cipher shifts letters by "
                                                                                "a fixed number in the alphabet."},
    {"id": 2, "caption": "Method ", "json_params": {"text": "str", "keyword": "str"}, "descriptions": "The Vigenère Cipher uses a keyword to shift "
                                                                       "letters variably."}
]


@app.post("/add_user")
def add_user(user: List[Users]):
    fake_users.extend(user)
    return {"status": 200, "data": fake_users}


@app.get("/list_users")
def get_list_users():
    users_without_secret = []
    for user in fake_users:
        new_user = {}
        for key, value in user.items():
            if key != "secret":
                new_user[key] = value
        users_without_secret.append(new_user)
    return users_without_secret


@app.get("/get_methods")
def get_methods():
    return methods_of_encryptions


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

