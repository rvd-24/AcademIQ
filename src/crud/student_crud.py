from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload
from src.models.student import Student
from src.models.user import User, UserTypeEnum
import bcrypt


def hash_password(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode('utf-8')  # Convert bytes to string for storage


async def create_student_with_user(
    db: AsyncSession,
    email: str,
    password: str,
    full_name: str,
    registration_number: str,
    department: str,
    batch_year: int
):
    """Create user and student in one transaction (async)"""
    user = User(
        email=email,
        password_hash=hash_password(password),
        user_type=UserTypeEnum.STUDENT,
        full_name=full_name
    )
    db.add(user)
    # Flush to populate PK on user
    await db.flush()

    student = Student(
        user_id=user.user_id,
        registration_number=registration_number,
        department=department,
        batch_year=batch_year
    )
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return student


async def get_student_by_registration(db: AsyncSession, reg_no: str):
    """Get student with user details (async)"""
    stmt = select(Student).where(Student.registration_number == reg_no).options(joinedload(Student.user))
    result = await db.execute(stmt)
    return result.scalars().first()


async def get_student_with_marksheets(db: AsyncSession, student_id: str):
    """Get student with all marksheets and marks (async)"""
    from src.models.marksheet import Marksheet

    stmt = (
        select(Student)
        .where(Student.student_id == student_id)
        .options(
            joinedload(Student.user),
            joinedload(Student.marksheets).joinedload(Marksheet.marks)
        )
    )
    result = await db.execute(stmt)
    return result.scalars().first()


async def update_student_department(db: AsyncSession, student_id: str, new_department: str):
    stmt = select(Student).where(Student.student_id == student_id)
    result = await db.execute(stmt)
    student = result.scalars().first()
    if student:
        student.department = new_department
        await db.commit()
        await db.refresh(student)
    return student


async def delete_student(db: AsyncSession, student_id: str):
    stmt = select(Student).where(Student.student_id == student_id)
    result = await db.execute(stmt)
    student = result.scalars().first()
    if student:
        await db.delete(student)
        await db.commit()
        return True
    return False