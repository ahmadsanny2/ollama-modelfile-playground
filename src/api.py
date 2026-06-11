import psutil
from ollama import chat
from fastapi import FastAPI
import uvicorn

app = FastAPI()


def get_temperature(kota: str) -> str:
    """mendapatkan suhu di kota tertentu

    Args:
        kota (str): nama kota yang ingin diketahui suhunya

    Returns:
        suhu saat ini untuk kota tersebut atau 'unknown' jika tidak ditemukan
    """

    temperature = {
        "bandung": "22 derajat celcius",
        "jakarta": "30 derajat celcius",
        "manokwari": "32 derajat celcius ",
    }

    return temperature.get(kota, "unknown")


def get_pc_status():
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    return {"CPU (%)": cpu, "RAM (%)": ram, "Disk (%)": disk}

@app.get("/chat")
def chat_ai(prompt: str):
    messages=[{"role": "user", "content": prompt}]
    tool_list=[get_pc_status, get_temperature]
    response=chat(model= "gemma4:12b", messages= messages, tools= tool_list)
    
    messages.append(response.message)
    if response.message.tool_calls:
        call = response.message.tool_calls[0]
        tool_name = call.function.name
        tool_arg = call.function.arguments

        print(tool_name)
        print(tool_arg)

    if tool_name == "get_pc_status":
        result = get_pc_status()
    elif tool_name == "get_temperature":
        result = get_temperature(tool_arg["kota"])
    else:
        result = "Tool tidak tersedia!"

    messages.append({"role": "tool", "tool_name": tool_name, "content": str(result)})

    final_response = chat(
        model="gemma4:12b",
        messages=messages,
        tools=tool_list,
        think=False,
    )

    return{
        "response":final_response.message.content
    }
    
if __name__ == "__main__":
    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=8080,
        reload=True
    )