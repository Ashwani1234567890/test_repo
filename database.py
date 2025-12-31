import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Fetch Environment Variables from Render
TURSO_DB_URL = os.environ.get("TURSO_DATABASE_URL")
TURSO_DB_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")

if not TURSO_DB_URL or not TURSO_DB_TOKEN:
    raise ValueError("Missing TURSO_DATABASE_URL or TURSO_AUTH_TOKEN in environment variables.")

# 2. Construct the LibSQL Connection String
# IMPORTANT: Python 3.13 requires the 'sqlalchemy-libsql' dialect package 
# to handle the 'sqlite+libsql://' prefix correctly.
# We also ensure the mandatory '/' before the '?' to avoid 308 Redirects.
clean_url = TURSO_DB_URL.replace("libsql://", "").replace("https://", "")
connection_string = f"sqlite+libsql://{clean_url}/?authToken={TURSO_DB_TOKEN}"

# 3. Create the SQLAlchemy Engine
# pool_pre_ping=True checks connection health before use (crucial for cloud DBs)
engine = create_engine(
    connection_string,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True
)

# 4. Setup Session and Base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 5. Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

