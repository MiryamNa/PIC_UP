from bson import ObjectId
from models.event import Event
from dto.EventDTO import EventDTO

class EventRepository:

    async def create_event(self, dto: EventDTO):

        event = Event(
            clientId=dto.clientId,
            name=dto.name,
            quantityPictureChoose=dto.quantityPictureChoose,
            totalPictures=dto.totalPictures,
            pathToFolder=dto.pathToFolder
        )

        await event.insert()
        print(event)
        return event

    async def get_event(self, event_id: str):
        return await Event.get(ObjectId(event_id))

    async def get_all_events(self):
        return await Event.find_all().to_list()

    async def update_event(self, event_id: str, update_data: dict):
        event = await Event.get(ObjectId(event_id))
        if event:
            await event.update({"$set": update_data})
            return event
        return None

    async def delete_event(self, event_id: str):
        event = await Event.get(ObjectId(event_id))
        if event:
            await event.delete()
            return True
        return False