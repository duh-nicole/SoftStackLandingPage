from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Creates a local SQLite file named onboarding.db in your backend folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./onboarding.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to yield database sessions to our API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


