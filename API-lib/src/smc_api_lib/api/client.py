"""Клиент для взаимодействия с SMC сервисом"""

from typing import Optional, Dict, Any
import requests
from smc_api_lib.schemas.api_schemas import (
    GenerateRequest,
    GenerateResponse
)


class SMCClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({'Authorization': f'Bearer {api_key}'})
        
        self.session.headers.update({'User-Agent': 'SMC-API-Client/1.0.0'})

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault('timeout', self.timeout)
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else {}

    def upload_file(self, file_path: str) -> str:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.split('/')[-1], f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
            result = self._request('POST', '/api/v1/documents/upload', files=files)
        return result['file_path']

    def get_disciplines(self, file_path: str) -> list:
        result = self._request('POST', '/api/v1/documents/disciplines', 
                              json={'file_path': file_path})
        return result['disciplines']

    def generate(self, request: GenerateRequest) -> GenerateResponse:
        result = self._request('POST', '/api/v1/documents/generate',
                              json=request.model_dump())
        return GenerateResponse(**result)

    def download_file(self, filename: str, save_path: str) -> bool:
        response = self.session.get(
            f"{self.base_url}/api/v1/documents/download/{filename}",
            stream=True,
            timeout=self.timeout
        )
        
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        return False