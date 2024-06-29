from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, JSON, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from config import DATABASE_URL

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Models
class UserORM(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(30), unique=True, nullable=False)
    secret = Column(String, nullable=False)


class MethodOfEncryptionORM(Base):
    __tablename__ = 'methods_of_encryption'
    id = Column(Integer, primary_key=True, index=True)
    caption = Column(String(30), nullable=False)
    json_params = Column(JSON, nullable=False)
    description = Column(String(1000), nullable=False)


class SessionORM(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    method_id = Column(Integer, nullable=False)
    data_in = Column(String, nullable=False)
    params = Column(JSON, nullable=False)
    data_out = Column(String, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    time_op = Column(Float, nullable=False)


# Create all tables if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Сервис для шифрования и дешифрования текста.")

ALPHABET = " ,.:(_)-0123456789АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


# Pydantic models
class User(BaseModel):
    id: int
    login: str = Field(min_length=3, max_length=30)
    secret: str


class MethodOfEncryption(BaseModel):
    id: int
    caption: str = Field(max_length=30)
    json_params: dict
    description: str = Field(max_length=1000)


class Session(BaseModel):
    id: int
    user_id: int
    method_id: int
    data_in: str
    params: dict
    data_out: str
    status: int
    created_at: datetime
    time_op: float


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/add_users")
async def add_user(users: List[User], db: Session = Depends(get_db)):
    try:
        for user in users:
            existing_user = db.query(UserORM).filter(UserORM.login == user.login).first()
            if existing_user:
                raise HTTPException(status_code=400, detail=f"Login '{user.login}' is already in use")

            new_user = UserORM(login=user.login, secret=user.secret)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": 200, "data": users}


@app.get("/list_users")
async def get_list_users(db: Session = Depends(get_db)):
    try:
        users = db.query(UserORM).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_methods")
async def get_methods(db: Session = Depends(get_db)):
    try:
        methods = db.query(MethodOfEncryptionORM).all()
        return methods
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def identification_user(login: str, secret: str, db: Session):
    try:
        user = db.query(UserORM).filter(UserORM.login == login, UserORM.secret == secret).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid login or secret")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def session_caesar(user, text_before_operation, number_of_shifts, text_after_operation_str, db: Session):
    try:
        session = SessionORM(
            user_id=user.id,
            method_id=1,
            data_in=text_before_operation,
            params={"text": text_before_operation, "shifts": number_of_shifts},
            data_out=text_after_operation_str,
            status=200,
            created_at=datetime.now(),
            time_op=0.0
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/encrypt/caesar")
async def encrypt_caesar_method(text_for_encrypt: str, number_of_shifts: int, login: str, secret: str,
                                db: Session = Depends(get_db)):
    try:
        user = await identification_user(login, secret, db)
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
        session = await session_caesar(user, text_for_encrypt, number_of_shifts, encrypted_text_str, db)
        return {"status": 200, "data": encrypted_text_str}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/decrypt/caesar")
async def decrypt_caesar_method(text_for_decrypt: str, number_of_shifts: int, login: str, secret: str,
                                db: Session = Depends(get_db)):
    try:
        user = await identification_user(login, secret, db)
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
        session = await session_caesar(user, text_for_decrypt, number_of_shifts, decrypted_text_str, db)
        return {"status": 200, "data": decrypted_text_str}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def session_vigenere(user, text_before_operation, keyword, text_after_operation_str, db: Session):
    try:
        session = SessionORM(
            user_id=user.id,
            method_id=2,
            data_in=text_before_operation,
            params={"text": text_before_operation, "keyword": keyword},
            data_out=text_after_operation_str,
            status=200,
            created_at=datetime.now(),
            time_op=0.0
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/encrypt/vigenere")
async def encrypt_vigenere_method(text_for_encrypt: str, keyword: str, login: str, secret: str,
                                  db: Session = Depends(get_db)):
    try:
        user = await identification_user(login, secret, db)
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
        session = await session_vigenere(user, text_for_encrypt, keyword, encrypted_text_str, db)
        return {"status": 200, "data": encrypted_text_str}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/decrypt/vigenere")
async def decrypt_vigenere_method(text_for_decrypt: str, keyword: str, login: str, secret: str,
                                  db: Session = Depends(get_db)):
    try:
        user = await identification_user(login, secret, db)
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
        session = await session_vigenere(user, text_for_decrypt, keyword, decrypted_text_str, db)
        return {"status": 200, "data": decrypted_text_str}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_session/{session_id}")
async def get_session(session_id: int, login: str, secret: str, db: Session = Depends(get_db)):
    try:
        user = await identification_user(login, secret, db)
        session = db.query(SessionORM).filter(SessionORM.id == session_id, SessionORM.user_id == user.id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found or access denied")
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/list_sessions")
async def list_sessions(login: str, secret: str, db: Session = Depends(get_db)):
    try:
        user = await identification_user(login, secret, db)
        sessions = db.query(SessionORM).filter(SessionORM.user_id == user.id).all()
        return sessions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def identification_user_without_login(secret: str, db: Session):
    try:
        user = db.query(UserORM).filter(UserORM.secret == secret).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid secret")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/delete_session/{session_id}")
async def delete_session(session_id: int, secret: str, db: Session = Depends(get_db)):
    try:
        user = await identification_user_without_login(secret, db)
        session = db.query(SessionORM).filter(SessionORM.id == session_id, SessionORM.user_id == user.id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found or access denied")
        db.delete(session)
        db.commit()
        return {"status": 200, "message": "Session deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
    try:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
