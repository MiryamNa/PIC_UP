from typing import List, Optional
from pydantic import BaseModel

class CategorySelection(BaseModel):
    category_name: str
    selected_count: int

class EventDTO(BaseModel):
    # legacy fields
    clientId: str
    name: str
    quantityPictureChoose: int
    totalPictures: int
    pathToFolder: str

    # new fields — album creation
    categories: List[CategorySelection] = []
    bride_image: Optional[str] = None       # base64
    groom_image: Optional[str] = None       # base64
    families: List[str] = []         # base64


