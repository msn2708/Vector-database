from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from get_config import Config
import threading

class SessionFactory(object):
    _self = None
    _engine = None
    _lock = threading.Lock()  # Create a lock for thread safety
    
    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self
    
    def __init__(self):
        with self._lock:  # Acquire the lock before initializing the object
            if self._engine is None:
                self._engine = create_engine(Config().get_config().get('db_url'))
    
    def get_session(self):
        return sessionmaker(bind=self._engine)()  # Bind the engine when creating a session
    
    def get_engine(self):
        return self._engine

    