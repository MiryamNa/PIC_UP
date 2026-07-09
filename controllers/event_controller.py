from fastapi import APIRouter, HTTPException
from services.event_service import EventService
from services.face_selected import FaceSelectedService
from pathlib import Path
from dto.EventDTO import EventDTO
from dto.buildRequestDTO import BuildRequest
from dto.face_selectedDTO import face_selectedDTO
from dto.FolderRequest import FolderRequest
from fastapi.responses import JSONResponse
import tkinter as tk
from tkinter import filedialog

service=FaceSelectedService()
router = APIRouter(prefix="/event", tags=["Events"])
# from services.build import Build

event_service = EventService()
#buildService = Build()
@router.post("/get_faces")
async def get_faces(event_data: EventDTO):
    return await event_service.get_faces(event_data)
# @router.post("/")
# async def create_event(event_data: EventDTO):
#     return await event_service.create_event(event_data)
@router.post("/")
async def create_event(event_data: EventDTO):
    """יצירת אירוע + בניית אלבום — מסיר כפילויות, מנקד, מפיץ לקטגוריות."""
    try:
        result = await event_service.build_album(event_data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))






# @router.post("/process-selection")
# async def process_faces(data:face_selectedDTO):
#     try:
#         result =service.process_selected_faces(
#             data.bride_image,
#             data.groom_image,
#             data.selected_faces
#         )
#         return result
#
#     except Exception as e:
#             return {"error": str(e)}


selected_folder = None
@router.post("/select-folder")
def select_folder():
    global selected_folder

    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', True)

    folder = filedialog.askdirectory(title="בחר תיקייה עם תמונות")
    root.destroy()

    print(folder)

    if not folder:
        return JSONResponse(content={"success": False})

    selected_folder = folder
    return JSONResponse(content={"success": True, "path": folder})
@router.get("/")
async def get_events():
    return await event_service.list_events()

@router.get("/{event_id}")
async def get_event(event_id: int):
    event = await event_service.get_event_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/{event_id}")
async def update_event(event_id: int, update_data: dict):
    event = await event_service.update_event(event_id, update_data)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.delete("/{event_id}")
async def delete_event(event_id: str):
    success = await event_service.remove_event(event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event deleted"}

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff"}
@router.post("/count-images")
async def count_images(data:FolderRequest):
    folder = Path(data.path)

    if not folder.exists():
        return {"error": "Folder does not exist"}

    if not folder.is_dir():
        return {"error": "Path is not a directory"}

    image_count = sum(
        1
        for file in folder.iterdir()
        if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS
    )

    return {"image_count": image_count}



# @router.post("/build/images")
# async def build_images(request: BuildRequest):
#     """
#     בנה דמויות לאירוע עם path, cust_id, event_id
#
#     :param request: BuildRequest עם path, cust_id, event_id
#     :return: תוצאות העיבוד
#     """
#     result = buildService.build_event_images(
#         path=request.path,
#         cust_id=request.cust_id,
#         event_id=request.event_id
#     )
#
#     # if result.get("status") == "error":
#     #     raise HTTPException(status_code=400, detail=result.get("message"))
#
#     return result