from fastapi import FastAPI

app = FastAPI(
    title="Сервис для шифрования"
)

@app.get("/user")
def index():
    pass