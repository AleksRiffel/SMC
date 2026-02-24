"""Pydantic схемы для API запросов и ответов"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class GenerateRequest(BaseModel):
    excel_file_path: str
    discipline_name: str
    template_rp: Optional[str] = "шаблонРП.docx"
    template_a: Optional[str] = "шаблонА.docx"
    template_fos: Optional[str] = "шаблонФОС.docx"


class GenerateResponse(BaseModel):
    success: bool
    message: str
    output_files: Dict[str, str]
    download_urls: Dict[str, str]
    discipline_info: Optional[Dict[str, Any]] = None


class UploadResponse(BaseModel):
    filename: str
    file_path: str


class DisciplinesResponse(BaseModel):
    disciplines: List[str]