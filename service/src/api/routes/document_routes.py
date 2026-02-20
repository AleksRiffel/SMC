from fastapi import APIRouter, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import FileResponse
import os
import shutil
from ...services.document_service import DocumentService
from ...core.config import settings
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])
document_service = DocumentService()

class GenerateRequest(BaseModel):
    excel_file_path: str
    discipline_name: str

class FilePathRequest(BaseModel):
    excel_file_path: str

@router.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Only Excel files are allowed")
    
    file_path = os.path.join(settings.UPLOADS_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"filename": file.filename, "file_path": file_path}

@router.post("/disciplines")
async def get_disciplines(request: FilePathRequest):
    try:
        disciplines = document_service.get_disciplines_from_excel(request.excel_file_path)
        return {"disciplines": disciplines}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate")
async def generate_documents(request: GenerateRequest):
    try:
        result = document_service.generate_documents(
            excel_path=request.excel_file_path,
            discipline_name=request.discipline_name
        )
        
        return {
            "success": True,
            "message": "Documents generated successfully",
            "output_files": {
                "rp": os.path.basename(result["rp"]),
                "a": os.path.basename(result["a"]),
                "fos": os.path.basename(result["fos"])
            },
            "discipline_info": result["discipline_info"]
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