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
        # create posts table
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS posts (
                        postID INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(255),
                        location VARCHAR(255),
                        imageURL VARCHAR(255),
                        description TEXT,
                        likesCount INT,
                        date VARCHAR(50)
                    );
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

class post_form(BaseModel):
    username: str
    location: str
    imageURL: str
    description: str
    likesCount: int
    date: str

# route checks if server running
@app.get("/")
def root():
    return {"message": "Server is running!"}

# login route
@app.post("/api/login")
def login(data: login_form):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT password FROM users WHERE username=%s",
                (data.username,)
            )
            user = cur.fetchone()

        # no user was found
        if not user:
            return {"message": "Username or password is incorrect!"}
        
        # if user found, we want to check the password hash
        pw_hash = user['password']
        if bcrypt.checkpw(data.password.encode("utf-8"), pw_hash.encode("utf-8")):
            return {"message": "Login successful!",
                        "status": "success","username": data.username}
        else:
            return {"message": "Login unsuccessful, wrong password!",
                        "status": "failed"
                        }
    finally:
        conn.close()

# signup route
@app.post("/api/signup")
def signup(data: signup_form):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            pw_hash = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            
            cur.execute("SELECT * from users where username = %s or email = %s or phoneNumber = %s", (data.username, data.email, data.phoneNumber))
            user = cur.fetchone()
            if user:
                return {"message": f"{data.email} already exists!"}
            else:
                cur.execute("INSERT INTO users (firstName, lastName, username, email, phoneNumber, password) VALUES (%s, %s, %s, %s, %s, %s)", (data.firstName, data.lastName, data.username, data.email, data.phoneNumber, pw_hash))
                conn.commit()   # Always commit for schema changes
                return {"message": f"{data.email} created!"}
    finally:
        conn.close()

@app.post("/api/post")
def post(data: post_form):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO posts(username, location, imageURL, description, likesCount, date) VALUES (%s, %s, %s, %s, %s, %s)", (data.username, data.location, data.imageURL, data.description, data.likesCount, data.date))
            conn.commit()
            return{'message': "Post Created!"}
    finally:
        conn.close()
    
    
  
