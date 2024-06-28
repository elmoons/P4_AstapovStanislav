from datetime import datetime
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


ALPHABET = " ,.:(_)-0123456789АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
EXITING_LOGINS = ["bob1997", "carl-stalker1337", "ivan_v_tanke"]


app = FastAPI(
    title="Сервис для шифрования и дешифрования текста."
)


class Users(BaseModel):
    id: int
    login: str = Field(min_length=3, max_length=30)
    secret: str


class MethodsOfEncryption(BaseModel):
    id: int
    caption: str = Field(max_length=30)
    json_params: dict
    description: str = Field(max_length=1000)


class Sessions(BaseModel):
    id: int
    user_id: int
    method_id: int
    data_in: str
    params: dict
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
    {"id": 1, "caption": "Method of Caesar", "json_params": {"text": "str", "shifts": "int"}, "description": "The Caesar Cipher shifts letters by "
                                                                                "a fixed number in the alphabet."},
    {"id": 2, "caption": "Method of Vigenere", "json_params": {"text": "str", "keyword": "str"}, "description": "The Vigenère Cipher uses a keyword to shift "
                                                                       "letters variably."}
]


sessions = [
    {"id": 1, "user_id": 2, "method_id": 1, "data_in": "ПРИВЕТ", "params": {"text": "ПРИВЕТ", "shifts": 3}, "data_out": "МНЁ9ВП", "status": 200, "created_at": "2024-06-16 15:34:12.345678", "time_op": 0.21},
    {"id": 2, "user_id": 1, "method_id": 1, "data_in": "ЁЛКА И ЛАМПОЧКА", "params": {"text": "ЁЛКА И ЛАМПОЧКА", "shifts": 1337}, "data_out": "5БА-Х8ХБ-ВЕДМА-", "status": 200, "created_at": "2024-06-16 16:54:17.123678", "time_op": 0.27},
    {"id": 3, "user_id": 3, "method_id": 2, "data_in": "КАРЛ УКРАЛ КАРАЛЫ", "params": {"text": "КАРЛ УКРАЛ КАРАЛЫ", "keyword": "КЛАР"}, "data_out": "-Э.6К9ЬБЬ1А5Ь6С6Ё", "status": 200, "created_at": "2024-05-23 17:25:14.243865", "time_op": 0.22},
]


@app.post("/add_users")
def add_user(users: List[Users]):
    for user in users:
        if user.login in [u['login'] for u in fake_users]:
            raise HTTPException(status_code=400, detail=f"Login '{user.login}' is already in use")
        fake_users.append(user.dict())
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


def identification_user(login: str, secret: str):
    user = next((u for u in fake_users if u["login"] == login and u["secret"] == secret), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid login or secret")
    return user


def session_caesar(user, text_before_operation, number_of_shifts, text_after_operation_str):
    session = {
        "id": len(sessions) + 1,
        "user_id": user["id"],
        "method_id": 1,
        "data_in": text_before_operation,
        "params": {"text": text_before_operation, "shifts": number_of_shifts},
        "data_out": text_after_operation_str,
        "status": 200,
        "created_at": datetime.now(),
        "time_op": 0.0
    }
    return session


@app.get("/encrypt/caesar")
def encrypt_caesar_method(text_for_encrypt: str, number_of_shifts: int, login: str, secret: str):
    user = identification_user(login, secret)
    text_for_encrypt_upper = text_for_encrypt.upper()
    encrypted_text = []
    alphabet_size = len(ALPHABET)

    for char in text_for_encrypt_upper:
        if char in ALPHABET:
            original_index = ALPHABET.index(char)
            new_index = (original_index + number_of_shifts) % alphabet_size
            encrypted_text.append(ALPHABET[new_index])
        else:
            encrypted_text.append(char)

    encrypted_text_str = ''.join(encrypted_text)
    session = session_caesar(user, text_for_encrypt, number_of_shifts, encrypted_text_str)
    sessions.append(session)

    return {"status": 200, "data": encrypted_text_str, "sessions": sessions}


@app.get("/decrypt/caesar")
def decrypt_caesar_method(text_for_decrypt: str, number_of_shifts: int, login: str, secret: str):
    user = identification_user(login, secret)
    text_for_decrypt_upper = text_for_decrypt.upper()
    decrypted_text = []
    alphabet_size = len(ALPHABET)

    for char in text_for_decrypt_upper:
        if char in ALPHABET:
            encrypted_index = ALPHABET.index(char)
            new_index = (encrypted_index - number_of_shifts) % alphabet_size
            decrypted_text.append(ALPHABET[new_index])
        else:
            decrypted_text.append(char)

    decrypted_text_str = ''.join(decrypted_text)
    session = session_caesar(user, text_for_decrypt, number_of_shifts, decrypted_text_str)
    sessions.append(session)

    return {"status": 200, "data": decrypted_text_str, "sessions": sessions}


def session_vigenere(user, text_before_operation, keyword, text_after_operation_str):
    session = {
        "id": len(sessions) + 1,
        "user_id": user["id"],
        "method_id": 2,
        "data_in": text_before_operation,
        "params": {"text": text_before_operation, "keyword": keyword},
        "data_out": text_after_operation_str,
        "status": 200,
        "created_at": datetime.now(),
        "time_op": 0.0
    }
    return session


@app.get("/encrypt/vigenere")
def encrypt_vigenere_method(text_for_encrypt: str, keyword: str, login: str, secret: str):
    user = identification_user(login, secret)
    text_for_encrypt_upper = text_for_encrypt.upper()
    keyword_upper = keyword.upper()
    encrypted_text = []
    alphabet_size = len(ALPHABET)
    keyword_len = len(keyword_upper)

    for i, char in enumerate(text_for_encrypt_upper):
        if char in ALPHABET:
            original_index = ALPHABET.index(char)
            key_char = keyword_upper[i % keyword_len]
            key_index = ALPHABET.index(key_char)
            new_index = (original_index + key_index) % alphabet_size
            encrypted_text.append(ALPHABET[new_index])
        else:
            encrypted_text.append(char)

    encrypted_text_str = ''.join(encrypted_text)
    session = session_vigenere(user, text_for_encrypt, keyword, encrypted_text_str)
    sessions.append(session)
    return {"status": 200, "data": encrypted_text_str, "sessions": sessions}


@app.get("/decrypt/vigenere")
def decrypt_vigenere_method(text_for_decrypt: str, keyword: str, login: str, secret: str):
    user = identification_user(login, secret)
    text_for_decrypt_upper = text_for_decrypt.upper()
    keyword_upper = keyword.upper()
    decrypted_text = []
    alphabet_size = len(ALPHABET)
    keyword_len = len(keyword_upper)

    for i, char in enumerate(text_for_decrypt_upper):
        if char in ALPHABET:
            encrypted_index = ALPHABET.index(char)
            key_char = keyword_upper[i % keyword_len]
            key_index = ALPHABET.index(key_char)
            new_index = (encrypted_index - key_index) % alphabet_size
            decrypted_text.append(ALPHABET[new_index])
        else:
            decrypted_text.append(char)

    decrypted_text_str = ''.join(decrypted_text)
    session = session_vigenere(user, text_for_decrypt, keyword, decrypted_text_str)
    sessions.append(session)

    return {"status": 200, "data": decrypted_text_str, "sessions": sessions}


@app.get("/get_session/{session_id}")
def get_session(session_id: int, login: str, secret: str):
    user = identification_user(login, secret)
    session = next((s for s in sessions if s["id"] == session_id and s["user_id"] == user["id"]), None)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or access denied")
    return session


def identification_user_without_login(secret: str):
    user = next((u for u in fake_users if u["secret"] == secret), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid login or secret")
    return user


@app.delete("/delete_session/{session_id}")
def delete_session(session_id: int, secret: str):
    user = identification_user_without_login(secret)
    session_index = next((i for i, s in enumerate(sessions) if s["id"] == session_id and s["user_id"] == user["id"]), None)
    if session_index is None:
        raise HTTPException(status_code=404, detail="Session not found or access denied")
    del sessions[session_index]
    return {"status": 200, "data": sessions}


def caesar_decrypt(text: str, shift: int) -> str:
    decrypted_text = []
    alphabet_size = len(ALPHABET)
    for char in text:
        if char in ALPHABET:
            encrypted_index = ALPHABET.index(char)
            new_index = (encrypted_index - shift) % alphabet_size
            decrypted_text.append(ALPHABET[new_index])
        else:
            decrypted_text.append(char)
    return ''.join(decrypted_text)


def vigenere_decrypt(text: str, keyword: str) -> str:
    decrypted_text = []
    alphabet_size = len(ALPHABET)
    keyword_len = len(keyword)
    keyword_upper = keyword.upper()

    for i, char in enumerate(text):
        if char in ALPHABET:
            encrypted_index = ALPHABET.index(char)
            key_char = keyword_upper[i % keyword_len]
            key_index = ALPHABET.index(key_char)
            new_index = (encrypted_index - key_index) % alphabet_size
            decrypted_text.append(ALPHABET[new_index])
        else:
            decrypted_text.append(char)

    return ''.join(decrypted_text)


@app.post("/hack")
def hack_text(text_for_hack: str, known_word: str) -> dict:
    known_word = known_word.upper()
    for shift in range(len(ALPHABET)):
        decrypted_text = caesar_decrypt(text_for_hack, shift)
        if known_word in decrypted_text:
            return {"method": "caesar", "shift": shift, "decrypted_text": decrypted_text}

    keyword_len_range = range(1, len(text_for_hack) // len(known_word) + 2)

    for keyword_len in keyword_len_range:
        for start_idx in range(len(text_for_hack) - len(known_word) + 1):
            substring = text_for_hack[start_idx:start_idx + len(known_word)]
            candidate_keyword = ''
            for i in range(len(known_word)):
                keyword_char = known_word[i]
                encrypted_char = substring[i]
                encrypted_index = ALPHABET.index(encrypted_char)
                key_char = keyword_char.upper()
                key_index = ALPHABET.index(key_char)
                new_index = (encrypted_index - key_index) % len(ALPHABET)
                candidate_keyword += ALPHABET[new_index]
            decrypted_text = vigenere_decrypt(text_for_hack, candidate_keyword)
            if known_word in decrypted_text:
                return {"method": "vigenere", "keyword": candidate_keyword, "decrypted_text": decrypted_text}

    return {"status": 404, "message": "Decryption failed"}
