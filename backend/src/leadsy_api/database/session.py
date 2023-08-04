from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from leadsy_api.core.config import get_settings

engine = create_engine(get_settings().database_uri, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
