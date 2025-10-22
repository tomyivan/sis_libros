from dataclasses import dataclass
from typing import List


@dataclass
class RecomendacionModeloDTO:
    libro_id: str
    score: float
    razones: List[str]
