from fastapi import FastAPI

app = FastAPI(title="My API")

@app.get("/")
def root():
    return {"message": "Hello, World!"}