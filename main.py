from datetime import datetime
from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="Сервис для шифрования"
)


class EncryptType(Enum):
    caesar: "caesar"
    vigenere: "vigenere"


class Users(BaseModel):
    id: int
    login: str = Field(min_length=3, max_length=30)
    secret: str


class MethodsOfEncryption(BaseModel):
    id: int
    caption: str
    json_params: dict
    descriptions: str


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


@app.get("/caesar")
def caesar_method(word_for_encrypt: str, number_of_shifts: int):
    word_for_encrypt_upper = word_for_encrypt.upper()
    alphabet = ",.:(_)-0123456789АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    encrypted_text = []
    alphabet_size = len(alphabet)

    for char in word_for_encrypt_upper:
        if char in alphabet:
            original_index = alphabet.index(char)
            new_index = (original_index + number_of_shifts) % alphabet_size
            encrypted_text.append(alphabet[new_index])
        else:
            encrypted_text.append(char)

    return ''.join(encrypted_text)


@app.get("/vigenere")
def vigenere_method(word_for_encrypt: str, keyword: str):
    word_for_encrypt_upper = word_for_encrypt.upper()
    keyword_upper = keyword.upper()
    alphabet = ",.:(_)-0123456789АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    encrypted_text = []
    alphabet_size = len(alphabet)
    keyword_len = len(keyword_upper)

    for i, char in enumerate(word_for_encrypt_upper):
        if char in alphabet:
            original_index = alphabet.index(char)
            key_char = keyword_upper[i % keyword_len]
            key_index = alphabet.index(key_char)
            new_index = (original_index + key_index) % alphabet_size
            encrypted_text.append(alphabet[new_index])
        else:
            encrypted_text.append(char)

    return ''.join(encrypted_text)
