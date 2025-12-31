import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from libsql_client import create_client

load_dotenv()

# 1. Get Environment Variables
TURSO_DB_URL = os.environ.get("libsql://testdb-yashu-05.aws-ap-south-1.turso.io")
TURSO_DB_TOKEN = os.environ.get("eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3NjcxNjc5NzksImlkIjoiOTNlNTA5Y2QtOWExMi00MDgyLTkzMDEtM2Y3M2U3ZjE4YzJiIiwicmlkIjoiMDA5Njc4NWYtY2EyMC00NDJmLWJiNzAtMGY1M2M2OTAzYjg4In0.044Var6bmTeuYEIaj5TUAcMkS0kBQLwdRbip6DW8AwsX34la-v_w2xKvJsyyYSZ0I6SqCL8im8re9UioAFGhBQ")

if not TURSO_DB_URL or not TURSO_DB_TOKEN:
    raise ValueError("TURSO_DATABASE_URL and TURSO_AUTH_TOKEN must be set in environment variables.")

def get_db_client():
    return create_client(url=URL, auth_token=TOKEN)

# 2. Format the URL for SQLAlchemy
# SQLAlchemy expects: sqlite+libsql://your-db-url.turso.io?authToken=your-token
# We strip 'libsql://' or 'https://' from the start if the user copied it directly.
clean_url = TURSO_DB_URL.replace("libsql://", "").replace("https://", "")
connection_string = f"sqlite+libsql://{clean_url}?authToken={TURSO_DB_TOKEN}"

# 3. Create the Engine
# check_same_thread=False is required for SQLite/LibSQL in multi-threaded apps (like FastAPI)
engine = create_engine(
    connection_string, 
    connect_args={"check_same_thread": False}
)

# 4. Create Session and Base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 5. Dependency for routes to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()







