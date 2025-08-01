from app.services.openai_llm import get_llm
llm = get_llm()
response = llm.invoke("What is the capital of Japan?")
print(response.content)  # Should return "Tokyo"
