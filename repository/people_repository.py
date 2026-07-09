class PeopleRepository:

    def __init__(self):
        self._store = {}

    async def save_selected(self, cust_id, event_id, embeddings):
        """Save all selected face embeddings (relatives)."""
        self._store[(cust_id, event_id)] = embeddings

    async def get_selected(self, cust_id, event_id):
        """Get all selected face embeddings (relatives)."""
        return self._store.get((cust_id, event_id), [])

    async def save_bride(self, cust_id, event_id, embedding):
        """Save bride face embedding."""
        self._store[(cust_id, event_id, "bride")] = embedding

    async def get_bride(self, cust_id, event_id):
        """Get bride face embedding."""
        return self._store.get((cust_id, event_id, "bride"))

    async def save_groom(self, cust_id, event_id, embedding):
        """Save groom face embedding."""
        self._store[(cust_id, event_id, "groom")] = embedding

    async def get_groom(self, cust_id, event_id):
        """Get groom face embedding."""
        return self._store.get((cust_id, event_id, "groom"))

people_repository = PeopleRepository()


