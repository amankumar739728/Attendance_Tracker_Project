from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from configs.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

db_session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))
