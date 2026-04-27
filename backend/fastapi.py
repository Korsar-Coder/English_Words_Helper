from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/words{user_name}")
def get_user_words(user_name: str):
    


uvicorn.run("backend/fastapi:app", reload=True)