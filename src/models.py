from dataclasses import dataclass
from typing import Any

@dataclass
class Task:
	id: int # уникальный номер
	payload: Any # данные