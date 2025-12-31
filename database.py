import os

# load dotenv locally only
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

TURSO_DB_URL = os.environ["TURSO_DATABASE_URL"]
TURSO_DB_TOKEN = os.environ["TURSO_AUTH_TOKEN"]

engine = create_engine(
    "sqlite+libsql://" + TURSO_DB_URL.replace("libsql://", ""),
    connect_args={"auth_token": TURSO_DB_TOKEN},
    pool_pre_ping=True
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# 4. FastAPI dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


