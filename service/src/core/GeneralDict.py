from pydantic import BaseModel
from typing import List

class ХарактеристикиОбъемаДисциплины(BaseModel):
    лекции: str
    практика: str
    лабраб: str
    самраб: str
    контроль: str
    аттестация: str
    семестр: str
    курс: str

class Компетенция(BaseModel):
    код: str
    описание: str

class GeneralDictModel(BaseModel):
    напрапвление: str
    профиль: str
    список_дисциплин: List[str]
    кафедры: List[str]
    форма_обучения: str
    выбранная_дисциплина: str
    компетенции: List[Компетенция]
    часы: str
    зачетные_единицы: str
    виды_занятий: List[ХарактеристикиОбъемаДисциплины]
    курсовая_работа: bool