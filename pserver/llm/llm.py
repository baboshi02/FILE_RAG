from langchain_groq import ChatGroq
from config import GROQ_MODEL


llm = ChatGroq(
    model=GROQ_MODEL,
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


def ask_llm(top_results_text: list[str], question: str):
    messages = [
        (
            "system",
            "You are a helpful assistant that uses RAG to answer questions provided from the following three top snippets answer the question",
        )
    ]
    messages.extend([("human", result) for result in top_results_text])
    messages.append(("human", question))
    response = llm.invoke(messages)
    return response.content
