from pathlib import Path
from fastapi import FastAPI, BackgroundTasks, Depends
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from src.routes import contacts, auth, users
from pydantic import EmailStr, BaseModel
from typing import List

import uvicorn
from dotenv import load_dotenv
import os

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis
from src.conf.config import settings
from fastapi.middleware.cors import CORSMiddleware
from src.conf.config import settings
import cloudinary

class EmailSchema(BaseModel):
    email: EmailStr

load_dotenv()
    
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", "youruser@meta.ua"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "yourpassword"),
    MAIL_FROM= os.getenv("MAIL_USERNAME", "youruser@meta.ua"),
    MAIL_PORT=465,
    MAIL_SERVER="smtp.meta.ua",
    MAIL_FROM_NAME="Example email",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)


app = FastAPI()

origins = [ 
    "http://localhost:3000"
    ]


app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/send-email")
async def send_in_background(background_tasks: BackgroundTasks, body: EmailSchema):
    message = MessageSchema(
        subject="Fastapi mail module",
        recipients=[body.email],
        template_body={"fullname": "Billy Jones"},
        subtype=MessageType.html
    )

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message, template_name="example_email.html")

    return {"message": "email has been sent"}


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)


@app.get("/")
def read_root():
    return {"message": "Hello World"}



if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.app_host, port=settings.app_port, reload=True)
