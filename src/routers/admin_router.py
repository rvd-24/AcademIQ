from DTO.admin_dto import UploadMarksheet
from services.admin_service import upload_file_process
@app.route("/",method=['GET'])
def admin_home(request: HomeAdmin):
    ...


@app.route("/upload",method=['POST'])
def upload_marksheet(request: UploadMarksheet):
    file_name = request.file_name
    user_id = request.user_id
    file_status = upload_file_process()
    # TODO File Upload to Blob and LLM based extraction and DB Insertion
    return "File Uploaded Successfully"