from fastapi import FastAPI
from recovery_api import router as recovery_router
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return{
        "message":"Revenue Recovery Agent is running"
    }

app.include_router(
    recovery_router,
    tags=["Recovery"]
)