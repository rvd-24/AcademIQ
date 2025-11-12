from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from models import Student, StudentMark, Subject, Marksheet

def get_student_semester_marks(db: Session, student_id: str, semester: int):
    """Get all marks for a student in a specific semester"""
    return db.query(StudentMark, Subject).join(
        Subject, StudentMark.subject_id == Subject.subject_id
    ).filter(
        and_(
            StudentMark.student_id == student_id,
            StudentMark.semester_number == semester
        )
    ).all()

def get_students_with_backlogs(db: Session, semester: int, subject_code: str = None):
    """Get students with backlogs"""
    query = db.query(Student, StudentMark, Subject).join(
        StudentMark, Student.student_id == StudentMark.student_id
    ).join(
        Subject, StudentMark.subject_id == Subject.subject_id
    ).filter(
        and_(
            StudentMark.has_backlog == True,
            StudentMark.semester_number == semester
        )
    )
    
    if subject_code:
        query = query.filter(Subject.subject_code == subject_code)
    
    return query.all()

def get_student_performance_summary(db: Session, student_id: str):
    """Get overall performance summary for a student"""
    return db.query(
        StudentMark.semester_number,
        func.count(StudentMark.mark_id).label('total_subjects'),
        func.avg(StudentMark.total_marks).label('average_marks'),
        func.sum(func.cast(StudentMark.has_backlog, Integer)).label('backlogs')
    ).filter(
        StudentMark.student_id == student_id
    ).group_by(
        StudentMark.semester_number
    ).all()

def get_top_performers_in_subject(db: Session, subject_code: str, semester: int, limit: int = 10):
    """Get top performers in a subject"""
    return db.query(Student, StudentMark).join(
        StudentMark, Student.student_id == StudentMark.student_id
    ).join(
        Subject, StudentMark.subject_id == Subject.subject_id
    ).filter(
        and_(
            Subject.subject_code == subject_code,
            StudentMark.semester_number == semester
        )
    ).order_by(StudentMark.total_marks.desc()).limit(limit).all()