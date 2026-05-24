from fastapi import APIRouter
from bson import ObjectId

from app.config.database import db
from app.schemas.student_schema import StudentCreate
from app.models.student_model import Student


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)



@router.post("/")
def create_student(student: StudentCreate):

    new_student = Student(
        nome=student.nome,
        turma=student.turma
    )

    result = db.students.insert_one(
        new_student.to_dict()
    )

    return {
        "message": "Aluno criado",
        "id": str(result.inserted_id)
    }


@router.get("/")
def get_students():

    students = list(db.students.find())

    for student in students:
        student["_id"] = str(student["_id"])

    return students




@router.get("/{student_id}")
def get_student(student_id: str):

    student = db.students.find_one({
        "_id": ObjectId(student_id)
    })

    if not student:
        return {
            "error": "Aluno não encontrado"
        }

    student["_id"] = str(student["_id"])

    return student


@router.put("/{student_id}")
def update_student(
    student_id: str,
    student: StudentCreate
):

    db.students.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": student.to_dict()}
    )

    return {
        "message": "Aluno atualizado"
    }



@router.delete("/{student_id}")
def delete_student(student_id: str):

    db.students.delete_one({
        "_id": ObjectId(student_id)
    })

    return {
        "message": "Aluno deletado"
    }

