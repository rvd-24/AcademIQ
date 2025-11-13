import os
import io
import fitz  # PyMuPDF
from azure.storage.blob import BlobServiceClient
from openai import AzureOpenAI
import base64
import json
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()


def upload_file_process(file_path: str):
    # === Step 1: Upload PDF to Azure Blob ===
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = "incoming"

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=os.path.basename(file_path))

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    blob_url = blob_client.url
    print(f"✅ Uploaded to Blob: {blob_url}")

    # === Step 2: Convert PDF to images using PyMuPDF ===
    pdf_doc = fitz.open(file_path)
    images = []

    for page_number in range(len(pdf_doc)):
        page = pdf_doc.load_page(page_number)
        pix = page.get_pixmap(dpi=200)  # You can increase dpi for sharper images
        img_bytes = io.BytesIO(pix.tobytes("png"))
        images.append(img_bytes)
    pdf_doc.close()

    print(f"📄 PDF converted to {len(images)} image(s) using PyMuPDF")

    # === Step 3: LLM Extraction ===
    client = AzureOpenAI(  # ✅ using AzureOpenAI
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )
    
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    extracted_data = []

    for idx, img_bytes in enumerate(images):
        img_bytes.seek(0)
        base64_img = base64.b64encode(img_bytes.read()).decode("utf-8")

        prompt = """
        You are an expert document parser. Extract the information from this student's marksheet image and return it strictly as a JSON object in this format:
        {
          "university": "...",
          "exam_info": {
            "exam_type": "...",
            "semester": <integer>,
            "announced_date": "YYYY-MM-DD"
          },
          "student_info": {
            "name": "...",
            "university_seat_number": "..."
          },
          "subjects": [
            {
              "subject_code": "...",
              "subject_name": "...",
              "internal_marks": <integer>,
              "external_marks": <integer>,
              "total": <integer>,
              "result": "P/F"
            }
          ],
          "summary": {
            "total_subjects": <integer>,
            "subjects_passed": <integer>,
            "status": "PASS/FAIL"
          }
        }
        """

        # ---- FIX: image_url must be an object with "url" key ----
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You extract structured data from university marksheets."},
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_img}"}}
                ]}
            ],
            max_tokens=2000,
            temperature=0
        )

        # Extract the assistant message (string)
        page_result = None
        try:
            page_result = response.choices[0].message.content
        except Exception:
            # be defensive: some SDKs / responses might differ; try alternative path
            page_result = getattr(response.choices[0].message, "content", None) or str(response)

        try:
            json_result = json.loads(page_result)
        except Exception:
            print(f"⚠️ JSON parsing failed for page {idx+1}. Raw output:")
            print(page_result)
            json_result = {"raw_text": page_result}

        extracted_data.append(json_result)

    # === Step 4: Combine multi-page results ===
    if len(extracted_data) == 1:
        final_result = extracted_data[0]
    else:
        final_result = {
            "pages": extracted_data,
            "combined_subjects": [s for page in extracted_data for s in page.get("subjects", [])]
        }

    print("✅ Extraction complete")
    return {
        "blob_url": blob_url,
        "extracted_json": final_result,
        "timestamp": datetime.utcnow().isoformat()
    }
