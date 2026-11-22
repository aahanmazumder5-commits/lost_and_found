from dataclasses import dataclass
from datetime import datetime


class LostFoundError(Exception):
    pass


class InvalidItemError(LostFoundError):
    pass


class RecordNotFoundError(LostFoundError):
    pass


class Item:
    _registered_count = 0

    def __init__(self, title="", description="", location="", contact="", item_id=None, created_at=None):
        self._item_id = item_id
        self.title = title.strip()
        self.description = description.strip()
        self.location = location.strip()
        self.contact = contact.strip()
        self.created_at = created_at or datetime.now().isoformat(timespec="seconds")
        if item_id is None:
            type(self)._registered_count += 1

    @property
    def item_id(self):
        return self._item_id

    @classmethod
    def registered_count(cls):
        return cls._registered_count

    def display_item(self):
        return f"#{self.item_id} · {self.title} · {self.location}"


class LostItem(Item):
    def __init__(self, title="", description="", location="", contact="", item_id=None, created_at=None, status="Open"):
        super().__init__(title, description, location, contact, item_id, created_at)
        self.status = status


class FoundItem(Item):
    def __init__(self, title="", description="", location="", contact="", item_id=None, created_at=None, status="Open"):
        super().__init__(title, description, location, contact, item_id, created_at)
        self.status = status


@dataclass
class User:
    name: str
    email: str

    def display_name(self):
        return self.name.strip() or self.email.strip()
