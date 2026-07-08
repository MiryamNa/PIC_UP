from pydantic import BaseModel

class FolderRequest(BaseModel):
    path: str