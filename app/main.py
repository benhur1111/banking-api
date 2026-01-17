from fastapi import FastAPI
from app.routes.bank import router

app = FastAPI(title="Banking API")

# Include the bank routes
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Banking API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
