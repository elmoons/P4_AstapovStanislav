from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Сервис для шифрования"
)


class Users(BaseModel):
    login = str
    secret = str



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
