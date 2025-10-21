from fastapi import FastAPI
import pymysql
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import bcrypt
from contextlib import asynccontextmanager


load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 5432))  # default port 5432 if missing
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# establish connection with database
def get_conn():
    timeout = 10
    return pymysql.connect(
    charset="utf8mb4",
    connect_timeout=timeout,
    cursorclass=pymysql.cursors.DictCursor,
    db=DB_NAME,
    host=DB_HOST,
    password=DB_PASS,
    read_timeout=timeout,
    port=DB_PORT,
    user=DB_USER,
    write_timeout=timeout,
)

# ---- Create table once on startup ----
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup code here ---
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            firstName VARCHAR(100),
            lastName VARCHAR(100),
            username VARCHAR(100) PRIMARY KEY,
            email VARCHAR(255) UNIQUE,
            phoneNumber VARCHAR(50) UNIQUE,
            password VARCHAR(255)
        )
        """)
    conn.commit()
    conn.close()

    yield

# api endpoints
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class signup_form(BaseModel):
    firstName: str
    lastName: str
    username: str
    email: str
    phoneNumber: str
    password: str

class login_form(BaseModel):
    username: str
    password: str


@app.get("/")
def root():
    return {"message": "Server is running!"}

@app.post("/api/login")
def login(data: login_form):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM users WHERE username=%s AND password=%s",
                (data.username, data.password)
            )
            user = cur.fetchone()

        if not user:
            return {"message": "Username or password is incorrect!"}

        return {"message": "Login successful!"}
    finally:
        conn.close()

@app.post("/api/signup")
def signup(data: signup_form):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            pw_hash = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            
            cur.execute("SELECT * from users where username = %s or email = %s or phoneNumber = %s", (data.username, data.email, data.phoneNumber))
            user = cur.fetchone()
            if user:
                return {"message": f"{data.username} already exists!"}
            else:
                cur.execute("INSERT INTO users (firstName, lastName, username, email, phoneNumber, password) VALUES (%s, %s, %s, %s, %s, %s)", (data.firstName, data.lastName, data.username, data.email, data.phoneNumber, pw_hash))
                conn.commit()   # Always commit for schema changes
                return {"message": f"{data.username} created!"}
    finally:
        conn.close()
    
  
