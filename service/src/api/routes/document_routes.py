from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
import os
import shutil
import uuid

from src.core.config import settings
from src.services.document_service import DocumentService

# Создаем роутер
router = APIRouter(prefix="/documents", tags=["documents"])
service = DocumentService()

@router.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Only Excel files are allowed")
    
    file_path = os.path.join(settings.UPLOADS_DIR, f"{uuid.uuid4()}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"filename": file.filename, "file_path": file_path}

@router.post("/disciplines")
async def get_disciplines(file_path: str):
    try:
        disciplines = service.get_disciplines_from_excel(file_path)
        return {"disciplines": disciplines}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate")
async def generate_documents(file_path: str, discipline_name: str):
    try:
        result = service.generate_documents(file_path, discipline_name)
        
        return {
            "success": True,
            "message": "Documents generated successfully",
            "output_files": {
                "rp": os.path.basename(result["rp"]),
                "a": os.path.basename(result["a"]),
                "fos": os.path.basename(result["fos"])
            },
            "download_urls": {
                "rp": f"/api/v1/documents/download/{os.path.basename(result['rp'])}",
                "a": f"/api/v1/documents/download/{os.path.basename(result['a'])}",
                "fos": f"/api/v1/documents/download/{os.path.basename(result['fos'])}"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(settings.GENERATED_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )