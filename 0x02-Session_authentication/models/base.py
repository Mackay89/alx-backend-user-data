from datetime import datetime
from typing import TypeVar, List, Iterable, Dict
from os import path
import json
import uuid
from threading import Lock

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATA: Dict[str, Dict[str, 'Base']] = {}
DATA_LOCK = Lock()

class Base:
    """Base class providing basic CRUD and serialization functionality."""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a Base instance."""
        s_class = self.__class__.__name__
        with DATA_LOCK:
            if DATA.get(s_class) is None:
                DATA[s_class] = {}

        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = datetime.strptime(kwargs.get('created_at'), TIMESTAMP_FORMAT) \
            if kwargs.get('created_at') else datetime.utcnow()
        self.updated_at = datetime.strptime(kwargs.get('updated_at'), TIMESTAMP_FORMAT) \
            if kwargs.get('updated_at') else datetime.utcnow()

    def __eq__(self, other: TypeVar('Base')) -> bool:
        """Check equality based on type and id."""
        return isinstance(other, Base) and self.id == other.id

    def to_json(self, for_serialization: bool = False) -> dict:
        """Convert the object to a JSON dictionary."""
        result = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key.startswith('_'):
                continue
            result[key] = value.strftime(TIMESTAMP_FORMAT) if isinstance(value, datetime) else value
        return result

    @classmethod
    def load_from_file(cls):
        """Load all objects from file."""
        s_class = cls.__name__
        file_path = f".db_{s_class}.json"
        with DATA_LOCK:
            DATA[s_class] = {}
            if not path.exists(file_path):
                return

            try:
                with open(file_path, 'r') as f:
                    objs_json = json.load(f)
                    for obj_id, obj_json in objs_json.items():
                        DATA[s_class][obj_id] = cls(**obj_json)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error loading file: {e}")

    @classmethod
    def save_to_file(cls):
        """Save all objects to file."""
        s_class = cls.__name__
        file_path = f".db_{s_class}.json"
        with DATA_LOCK:
            objs_json = {obj_id: obj.to_json(True) for obj_id, obj in DATA[s_class].items()}
            with open(file_path, 'w') as f:
                json.dump(objs_json, f)

    def save(self):
        """Save current object."""
        s_class = self.__class__.__name__
        self.updated_at = datetime.utcnow()
        with DATA_LOCK:
            DATA[s_class][self.id] = self
        self.__class__.save_to_file()

    def remove(self):
        """Remove object."""
        s_class = self.__class__.__name__
        with DATA_LOCK:
            if self.id in DATA[s_class]:
                del DATA[s_class][self.id]
        self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        """Count all objects."""
        s_class = cls.__name__
        with DATA_LOCK:
            return len(DATA[s_class])

    @classmethod
    def all(cls) -> Iterable[TypeVar('Base')]:
        """Return all objects."""
        return cls.search()

    @classmethod
    def get(cls, id: str) -> TypeVar('Base'):
        """Return one object by ID."""
        s_class = cls.__name__
        with DATA_LOCK:
            return DATA[s_class].get(id)

    @classmethod
    def search(cls, attributes: dict = {}) -> List[TypeVar('Base')]:
        """Search all objects with matching attributes."""
        s_class = cls.__name__
        
        def _search(obj):
            return all(getattr(obj, k) == v for k, v in attributes.items())
        
        with DATA_LOCK:
            return list(filter(_search, DATA[s_class].values()))
