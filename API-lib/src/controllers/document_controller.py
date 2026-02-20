from typing import Optional
import requests
from ..schemas.document_schemas import DocumentGenerationRequest, DocumentGenerationResponse

class DocumentController:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({'Authorization': f'Bearer {api_key}'})
    
    def generate_documents(self, request: DocumentGenerationRequest) -> DocumentGenerationResponse:
        response = self.session.post(
            f"{self.base_url}/api/v1/documents/generate",
            json=request.model_dump()
        )
        response.raise_for_status()
        return DocumentGenerationResponse(**response.json())
    
    def get_disciplines_list(self, excel_file_path: str) -> list:
        response = self.session.post(
            f"{self.base_url}/api/v1/documents/disciplines",
            json={"excel_file_path": excel_file_path}
        )
        response.raise_for_status()
        return response.json()["disciplines"]
    
    def download_generated_file(self, filename: str, save_path: str) -> bool:
        response = self.session.get(
            f"{self.base_url}/api/v1/documents/download/{filename}",
            stream=True
        )
        
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        return False