from typing import List
from pydantic import BaseModel

class face_selectedDTO(BaseModel):
    bride_image: str
    groom_image: str
    selected_faces: List[str]
