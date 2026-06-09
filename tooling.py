import psutil
from ollama import chat

def ambil_status_simpel():
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    
    return {"CPU (%)": cpu, "RAM (%)": ram, "DISK (%)": disk}

messages=[
    {
        "role":"user",
        "content":"Cek kondisi PC saya saat ini"
    }
]

response= chat(
    model="pcmonitor:v3",
    messages= messages,
    tools= [ambil_status_simpel]
)

messages.append(response.message)
if response.message.tool_calls:
    call = response.message.tool_calls[0]
    tool_name = call.function.name
    print(tool_name)
    
    result = ambil_status_simpel()
    
    messages.append(
        {
            "role":"tool",
            "tool_name":tool_name,
            "content":str(result)
        }
    )
    final_response = chat(
        model="pcmonitor:v3",
        messages=messages,
        tools=[ambil_status_simpel],
        think=False
        )
    print(f"[Tooling | AI Response]: {final_response.message.content}")
else:
    print(f"Non-Tooling | AI Response: {response.message.content}")