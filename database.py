import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Fetch Environment Variables
TURSO_DB_URL = os.environ.get("TURSO_DATABASE_URL")
TURSO_DB_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")

if not TURSO_DB_URL or not TURSO_DB_TOKEN:
    raise ValueError("Missing TURSO_DATABASE_URL or TURSO_AUTH_TOKEN")

# 2. DO NOT modify the URL
# It MUST stay libsql://xxxxx.turso.io
engine = create_engine(
    TURSO_DB_URL,
    connect_args={
        "auth_token": TURSO_DB_TOKEN
    },
    pool_pre_ping=True
)

# 3. Session and Base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 4. FastAPI dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
