from fastapi import FastAPI
import pymysql
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 5432))  # default port 5432 if missing
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# establish connection with database
timeout = 10
connection = pymysql.connect(
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



# api endpoints
app = FastAPI()

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

@app.get("/")
def root():
    return {"message": "Server is running!"}

@app.post("/api/signup")
def signup(data: signup_form):
    return {"message": f"Welcome, {data.firstName}!"}
  
"""try:
  cursor = connection.cursor()
  cursor.execute("DROP TABLE IF EXISTS mytest")
  connection.commit()   # Always commit for schema changes
  cursor.execute("SELECT * FROM mytest")
  print(cursor.fetchall())
finally:
  connection.close()"""