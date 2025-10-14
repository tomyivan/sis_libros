from dataclasses import dataclass
from datetime import datetime
from typing import Optional
@dataclass
class PublicacionModelo:
    mensaje: str
    fecha_creacion: datetime
    data: Optional[dict] = None