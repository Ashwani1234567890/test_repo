import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Fetch Environment Variables from Render
# Make sure these names match exactly what you typed in the Render Dashboard
TURSO_DB_URL = os.environ.get("TURSO_DATABASE_URL")
TURSO_DB_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")

if not TURSO_DB_URL or not TURSO_DB_TOKEN:
    raise ValueError("Missing TURSO_DATABASE_URL or TURSO_AUTH_TOKEN environment variables.")

# 2. Construct the LibSQL Connection String
# We must ensure the format: sqlite+libsql://[host]/?authToken=[token]
# Note: The '/' before the '?' is critical to avoid '308 Permanent Redirect' errors.
clean_url = TURSO_DB_URL.replace("libsql://", "").replace("https://", "").rstrip("/")
connection_string = f"sqlite+libsql://{clean_url}/?authToken={TURSO_DB_TOKEN}"

# 3. Create the SQLAlchemy Engine
# pool_pre_ping=True helps maintain the connection to a remote cloud DB
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
