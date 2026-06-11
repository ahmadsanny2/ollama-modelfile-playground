import psutil
from ollama import chat


def get_weather(kota: str) -> str:
    """mendapatkan suhu di kota tertentu

    Args:
        kota (str): nama kota yang ingin diketahui suhunya

    Returns:
        suhu saat ini untuk kota tersebut atau 'unknown' jika tidak ditemukan
    """

    weather = {
        "bandung": "22 derajat celcius",
        "jakarta": "30 derajat celcius",
        "manokwari": "32 derajat celcius ",
    }

    return weather.get(kota, "unknown")


def get_pc_status():
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    return {"CPU (%)": cpu, "RAM (%)": ram, "Disk (%)": disk}


messages = [{"role": "user", "content": "Berapa suhu di bandung?"}]
tool_list = [get_pc_status, get_weather]

response = chat(model="gemma4:12b", messages=messages, tools=tool_list, think=False)

messages.append(response.message)
if response.message.tool_calls:
    call = response.message.tool_calls[0]
    tool_name = call.function.name
    tool_arg = call.function.arguments

    print(tool_name)
    print(tool_arg)

    if tool_name == "get_pc_status":
        result = get_pc_status()
    elif tool_name == "get_weather":
        result = get_weather(tool_arg["kota"])
    else:
        result = "Tool tidak tersedia!"

    messages.append({"role": "tool", "tool_name": tool_name, "content": str(result)})

    final_response = chat(
        model="gemma4:12b",
        messages=messages,
        tools=tool_list,
        think=False,
    )

    print(final_response.message.content)
