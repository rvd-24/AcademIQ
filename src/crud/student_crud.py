from sqlalchemy.orm import Session
from models import Student, User, UserTypeEnum
from passlib.hash import bcrypt

def create_student_with_user(
    db: Session,
    email: str,
    password: str,
    full_name: str,
    registration_number: str,
    department: str,
    batch_year: int
):
    """Create user and student in one transaction"""
    
    # Create user
    user = User(
        email=email,
        password_hash=bcrypt.hash(password),
        user_type=UserTypeEnum.STUDENT,
        full_name=full_name
    )
    db.add(user)
    db.flush()  # Get user_id without committing
    
    # Create student
    student = Student(
        user_id=user.user_id,
        registration_number=registration_number,
        department=department,
        batch_year=batch_year
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    
    return student

def get_student_by_registration(db: Session, reg_no: str):
    """Get student with user details"""
    return db.query(Student).filter(
        Student.registration_number == reg_no
    ).first()

def get_student_with_marksheets(db: Session, student_id: str):
    """Get student with all marksheets and marks"""
    from sqlalchemy.orm import joinedload
    
    return db.query(Student).options(
        joinedload(Student.user),
        joinedload(Student.marksheets).joinedload(Marksheet.marks)
    ).filter(Student.student_id == student_id).first()

def update_student_department(db: Session, student_id: str, new_department: str):
    """Update student department"""
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if student:
        student.department = new_department
        db.commit()
        db.refresh(student)
    return student

def delete_student(db: Session, student_id: str):
    """Delete student (cascade deletes marks and marksheets)"""
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if student:
        db.delete(student)
        db.commit()
        return True
    return False