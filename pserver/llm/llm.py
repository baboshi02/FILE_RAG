from langchain_groq import ChatGroq
import os
import dotenv

dotenv.load_dotenv()

GROQ_MODEL = os.getenv("GROQ_MODEL") or ""
llm = ChatGroq(
    model=GROQ_MODEL,
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)
