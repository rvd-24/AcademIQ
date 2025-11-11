from pydantic import BaseModel
class UploadMarksheet(BaseModel):
    file_name: str
    user_id: str
    
