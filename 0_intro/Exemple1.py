from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="My First FastAPI Application",
    description="This is a simple FastAPI application example.",
    version="1.0.0",
    contact={
        "name": "Sidney Peres",
        "email": "sidney.peres@ufpr.br",
    }
)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
def read_item(name: str):
    return {"message": f"Hello, {name}!"}

if __name__ == "__main__":
    uvicorn.run("Exemple1:app", host="0.0.0.0", port=8000, reload=True)