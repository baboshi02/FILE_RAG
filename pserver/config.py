import os
import dotenv

dotenv.load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PC_MODEL = os.getenv("PC_MODEL")
JWT_SECRET = os.getenv("JWT_SECRET") or ""
DATABASE_URL = os.getenv("DATABASE_URL") or ""
GROQ_MODEL = os.getenv("GROQ_MODEL") or ""
