from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from get_config import get_config

# an Engine, which the Session will use for connection
# resources, typically in module scope
class SessionFactory(object):
    _self = None
    _engine = None
    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self
    
    def __init__(self):
        if(self._engine is None):
            _engine = create_engine(get_config().get('db_url'))
    
    def get_session(self):
        return sessionmaker(self._engine)