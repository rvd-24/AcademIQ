from sqlalchemy.orm import Session
from models import Marksheet, StudentMark, Subject, ProcessingStatusEnum
from datetime import date

def create_marksheet(
    db: Session,
    student_id: str,
    semester_number: int,
    blob_url: str,
    result_date: date = None
):
    """Create marksheet record after upload"""
    marksheet = Marksheet(
        student_id=student_id,
        semester_number=semester_number,
        blob_storage_url=blob_url,
        result_date=result_date,
        processing_status=ProcessingStatusEnum.PROCESSING
    )
    db.add(marksheet)
    db.commit()
    db.refresh(marksheet)
    return marksheet

def add_marks_from_llm_extraction(
    db: Session,
    marksheet_id: str,
    student_id: str,
    semester_number: int,
    extracted_marks: list
):
    """
    Add marks extracted by LLM
    
    extracted_marks format:
    [
        {
            "subject_code": "CS101",
            "subject_name": "Data Structures",
            "internal_marks": 25.0,
            "external_marks": 65.0,
            "total_marks": 90.0,
            "grade": "A",
            "has_backlog": False
        },
        ...
    ]
    """
    
    marks_objects = []
    
    for mark_data in extracted_marks:
        # Get or create subject
        subject = db.query(Subject).filter(
            Subject.subject_code == mark_data["subject_code"]
        ).first()
        
        if not subject:
            subject = Subject(
                subject_code=mark_data["subject_code"],
                subject_name=mark_data["subject_name"]
            )
            db.add(subject)
            db.flush()
        
        # Create mark record
        mark = StudentMark(
            student_id=student_id,
            marksheet_id=marksheet_id,
            subject_id=subject.subject_id,
            semester_number=semester_number,
            internal_marks=mark_data.get("internal_marks"),
            external_marks=mark_data.get("external_marks"),
            total_marks=mark_data.get("total_marks"),
            grade=mark_data.get("grade"),
            has_backlog=mark_data.get("has_backlog", False)
        )
        marks_objects.append(mark)
    
    # Bulk add marks
    db.bulk_save_objects(marks_objects)
    
    # Update marksheet status
    marksheet = db.query(Marksheet).filter(
        Marksheet.marksheet_id == marksheet_id
    ).first()
    marksheet.processing_status = ProcessingStatusEnum.COMPLETED
    
    db.commit()
    
    return marks_objects

def get_marksheet_with_marks(db: Session, marksheet_id: str):
    """Get complete marksheet with all marks and subject details"""
    from sqlalchemy.orm import joinedload
    
    return db.query(Marksheet).options(
        joinedload(Marksheet.marks).joinedload(StudentMark.subject)
    ).filter(Marksheet.marksheet_id == marksheet_id).first()


def insert_marksheet_data(
    db: Session,
    user_id: str,
    blob_url: str,
    extracted_data: dict
):
    # Get student_id from user_id
    student = db.query(Student).filter(Student.user_id == UUID(user_id)).first()
    if not student:
        raise ValueError("Student not found")
    
    # Create marksheet entry
    marksheet = Marksheet(
        student_id=student.student_id,
        semester_number=semester_number,
        result_date=extracted_data.get("result_date"),
        blob_storage_url=blob_url,
        processing_status="completed"
    )
    db.add(marksheet)
    db.flush()
    
    # Insert subjects and marks
    for subject_data in extracted_data["subjects"]:
        # Check if subject exists, create if not
        subject = db.query(Subject).filter(
            Subject.subject_code == subject_data["subject_code"]
        ).first()
        
        if not subject:
            subject = Subject(
                subject_code=subject_data["subject_code"],
                subject_name=subject_data["subject_name"]
            )
            db.add(subject)
            db.flush()
        
        # Insert student marks
        student_mark = StudentMark(
            student_id=student.student_id,
            marksheet_id=marksheet.marksheet_id,
            subject_id=subject.subject_id,
            semester_number=extracted_data['semester_number'],
            internal_marks=subject_data.get("internal_marks"),
            external_marks=subject_data.get("external_marks"),
            total_marks=subject_data["total_marks"],
            grade=subject_data.get("grade"),
            result_date=extracted_data.get("result_date"),
            has_backlog=subject_data.get("has_backlog", False)
        )
        db.add(student_mark)
    
    db.commit()
    return marksheet.marksheet_id