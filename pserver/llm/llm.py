from langchain_groq import ChatGroq
from config import GROQ_MODEL


llm = ChatGroq(
    model=GROQ_MODEL,
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)
