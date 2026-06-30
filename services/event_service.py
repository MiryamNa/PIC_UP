from collections import defaultdict

from dto.EventDTO import EventDTO
from repository.event_repository import EventRepository
from dto.EventDTO import EventDTO
from models.event import Event
from services.face_utils import extract_single_faces
from services.remove_duplicate import remove_duplicate_faces

class EventService:
    def __init__(self):
        self.repo = EventRepository()
    async def get_faces(self, event_data: EventDTO):
        faces = extract_single_faces(event_data.pathToFolder)
        faces= remove_duplicate_faces(faces)
        return faces

    async def create_event(self, event_data: EventDTO):

        return await self.repo.create_event(event_data)

    async def list_events(self):
        return await self.repo.get_all_events()

    async def get_event_by_id(self, event_id: int):
        return await self.repo.get_event(event_id)

    async def update_event(self, event_id: int, update_data: dict):
        return await self.repo.update_event(event_id, update_data)

    async def remove_event(self, event_id: int):
        return await self.repo.delete_event(event_id)