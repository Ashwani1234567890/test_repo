import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Try to load dotenv for local development
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# CORRECT: Pass the KEY name, not the value itself
TURSO_DB_URL = os.environ.get("TURSO_DATABASE_URL")
TURSO_DB_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")

if not TURSO_DB_URL or not TURSO_DB_TOKEN:
    raise ValueError("TURSO_DATABASE_URL and TURSO_AUTH_TOKEN must be set in environment variables.")

# Format for SQLAlchemy
# Remove 'libsql://' and prepend 'sqlite+libsql://'
clean_url = TURSO_DB_URL.replace("libsql://", "").replace("https://", "")
connection_string = f"sqlite+libsql://{clean_url}?authToken={TURSO_DB_TOKEN}"

engine = create_engine(
    connection_string, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




