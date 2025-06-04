from fastapi import FastAPI

# Krijo një instancë të klasës FastAPI
app = FastAPI()

# Rruga për URL-në rrënjë ("/") që përdor metodën HTTP GET
@app.get("/")
def root():
    return {"message": "Hello World"}

# Rruga që pranon një parameter 'name'
@app.get("/greet/")
def greet(name: str):
    return {"message": f"Hello, {name}!"}
