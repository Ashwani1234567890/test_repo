import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load .env only if running locally
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# We fetch by the KEY name
URL = os.environ.get("libsql://testdb-yashu-05.aws-ap-south-1.turso.io")
TOKEN = os.environ.get("eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3NjcxNjc5NzksImlkIjoiOTNlNTA5Y2QtOWExMi00MDgyLTkzMDEtM2Y3M2U3ZjE4YzJiIiwicmlkIjoiMDA5Njc4NWYtY2EyMC00NDJmLWJiNzAtMGY1M2M2OTAzYjg4In0.044Var6bmTeuYEIaj5TUAcMkS0kBQLwdRbip6DW8AwsX34la-v_w2xKvJsyyYSZ0I6SqCL8im8re9UioAFGhBQ")

# Debugging: This helps you see if the variables are actually loaded
if not URL or not TOKEN:
    print(f"DEBUG: URL found? {bool(URL)}")
    print(f"DEBUG: Token found? {bool(TOKEN)}")
    raise ValueError("TURSO_DATABASE_URL and TURSO_AUTH_TOKEN must be set in Render Environment Variables.")

# SQLAlchemy formatting for Turso
clean_url = URL.replace("libsql://", "").replace("https://", "")
connection_string = f"sqlite+libsql://{clean_url}?authToken={TOKEN}"

engine = create_engine(connection_string, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
