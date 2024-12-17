from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000/")  # Default to localhost:8000
DATABASE_URL = os.getenv("DATABASE_URL")