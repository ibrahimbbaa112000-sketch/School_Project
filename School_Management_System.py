from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Student(BaseModel):

    name:str
    age : int
    grade:float

def setup_database():
    try:
        conn = sqlite3.connect("school.db")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS students (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade FLOAT NOT NULL)
        """)
        conn.commit()


        conn.close()
    except sqlite3.Error as e :
        print(f"database setup error:{e}")
setup_database()

@app.get("/")
async def home():
    return FileResponse("Dashboard_for_school.html")

@app.get("/Students/")
async def Read_students():
    try:
        conn = sqlite3.connect("school.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        return {"Error":str(e)}


@app.post("/Students/")
async def create_student(new_student:Student):
    try:
        conn = sqlite3.connect("school.db")
        cursor = conn.cursor()
        cursor.execute("insert into students (name,age,grade) values (?,?,?)",(new_student.name,new_student.age,new_student.grade))
        conn.commit()
        conn.close()
        return {"message":"Student created"}
    except sqlite3.Error as e:
        print(e)
        return {"Error":"Failed to create student"}


@app.put("/Students/{student_id}")
async def update_student(student_id:int,new_student:Student):
    try:
        conn = sqlite3.connect("school.db")
        cursor = conn.cursor()
        cursor.execute("Update students set name = ?,age = ?,grade = ? where id = ?",
                       (new_student.name,new_student.age,new_student.grade,student_id))
        conn.commit()
        conn.close()
        return {"id":student_id,**new_student.dict()}
    except sqlite3.Error as e:
        print(e)
        return {"Error":"Failed to update student"}

@app.delete("/Students/{student_id}")
async def delete_student(student_id:int):
    try:
        conn = sqlite3.connect("school.db")
        cursor = conn.cursor()
        cursor.execute("delete from students where id = ?",(student_id,))
        conn.commit()
        conn.close()
        return {"message":"Student deleted"}
    except sqlite3.Error as e:
        print(e)
        return {"Error":"Failed to delete student"}


