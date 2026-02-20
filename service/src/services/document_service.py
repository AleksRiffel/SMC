import os
import uuid
from typing import List, Dict, Any
from ..utils import Workflow_functions as wf
from ..core.GeneralDict import GeneralDictModel
from ..core.config import settings

class DocumentService:
    def __init__(self):
        self.uploads_dir = settings.UPLOADS_DIR
        self.generated_dir = settings.GENERATED_DIR
        self.templates_dir = settings.TEMPLATES_DIR
        
        os.makedirs(self.uploads_dir, exist_ok=True)
        os.makedirs(self.generated_dir, exist_ok=True)
    
    def process_excel_file(self, excel_path: str, discipline_name: str) -> Dict[str, Any]:
        wb = wf.load_excel(excel_path)
        
        basic_info = wf.extract_basic_info(wb)
        specific_info = wf.extract_specific_info(wb)
        
        codes = wf.extract_competences(wb, discipline_name)
        competences = wf.fill_competences(wb, codes)
        
        volume_info = wf.fill_discipline_volume(wb, discipline_name)
        has_coursework = wf.check_coursework(wb, discipline_name)
        
        content = GeneralDictModel(
            напрапвление=basic_info["напрапвление"],
            профиль=basic_info["профиль"],
            список_дисциплин=basic_info["список дисциплин"],
            кафедры=basic_info["кафедры"],
            форма_обучения=specific_info["форма обучения"],
            выбранная_дисциплина=discipline_name,
            компетенции=competences,
            часы=volume_info["часы"],
            зачетные_единицы=volume_info["зачетные единицы"],
            виды_занятий=volume_info["виды занятий"],
            курсовая_работа=has_coursework
        )
        
        return content.model_dump()
    
    def generate_documents(self, excel_path: str, discipline_name: str) -> Dict[str, str]:
        content_data = self.process_excel_file(excel_path, discipline_name)
        content = GeneralDictModel(**content_data)
        
        file_id = str(uuid.uuid4())[:8]
        output_rp = os.path.join(self.generated_dir, f"RP_{discipline_name}_{file_id}.docx")
        output_a = os.path.join(self.generated_dir, f"A_{discipline_name}_{file_id}.docx")
        output_fos = os.path.join(self.generated_dir, f"FOS_{discipline_name}_{file_id}.docx")
        
        template_rp = os.path.join(self.templates_dir, "шаблонРП.docx")
        template_a = os.path.join(self.templates_dir, "шаблонА.docx")
        template_fos = os.path.join(self.templates_dir, "шаблонФОС.docx")
        
        wf.generate_documents(
            content=content,
            template_rp=template_rp,
            template_a=template_a,
            template_fos=template_fos,
            output_rp=output_rp,
            output_a=output_a,
            output_fos=output_fos
        )
        
        return {
            "rp": output_rp,
            "a": output_a,
            "fos": output_fos,
            "discipline_info": content_data
        }
    
    def get_disciplines_from_excel(self, excel_path: str) -> List[str]:
        wb = wf.load_excel(excel_path)
        basic_info = wf.extract_basic_info(wb)
        return basic_info["список дисциплин"]