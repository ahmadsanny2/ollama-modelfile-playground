from ollama import chat

response = chat(
    model="sanseni:v1",
    messages=[
        {
            "role": "user",
            "content": "Halo siapa kamu? Apa keunggulan kamu",
        },
        options={
            "temperature":0.2
        }
    ]
)

print(response.message.content)