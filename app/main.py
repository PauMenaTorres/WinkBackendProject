from fastapi import FastAPI

app = FastAPI(title="Wink Blog")

@app.get("/")
def read_root():
    return {"status": "ok"}