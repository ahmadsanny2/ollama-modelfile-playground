import psutil

def ambil_status_simpel():
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    
    return {"CPU (%)": cpu, "RAM (%)": ram, "DISK (%)": disk}

print(ambil_status_simpel())