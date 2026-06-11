from ollama import chat

response = chat(
    model="deaai:v1",
    messages=[{"role": "user", "content": "apakah kamu mengerti politik?"}],
    options={"temperature": 0.2},
)

print(response.message.content)
