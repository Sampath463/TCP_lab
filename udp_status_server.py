#!/usr/bin/python3
import socket
import psutil
import platform
import time
import datetime

# ================== System Info Functions ==================
def get_uptime():
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    return str(datetime.timedelta(seconds=int(uptime_seconds)))

def get_cpu_info():
    return {
        "Physical cores": psutil.cpu_count(logical=False),
        "Total cores": psutil.cpu_count(logical=True),
        "CPU usage (%)": psutil.cpu_percent(interval=1)
    }

def get_memory_info():
    mem = psutil.virtual_memory()
    return {
        "Total RAM (GB)": round(mem.total / (1024**3), 2),
        "Used RAM (GB)": round(mem.used / (1024**3), 2),
        "Available RAM (GB)": round(mem.available / (1024**3), 2),
        "RAM Usage (%)": mem.percent
    }

def get_hardware_info():
    return {
        "System": platform.system(),
        "Release": platform.release(),
        "Machine": platform.machine(),
        "Processor": platform.processor()
    }

def build_report():
    report = []
    report.append(f"Uptime: {get_uptime()}")
    report.append(f"CPU: {get_cpu_info()}")
    report.append(f"Memory: {get_memory_info()}")
    report.append(f"Hardware: {get_hardware_info()}")
    return "\n".join(report)

# ================== UDP Server ==================
IP = "0.0.0.0"   # listen on all interfaces
PORT = 9090

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))

print(f"UDP server listening on {IP}:{PORT} ...")

while True:
    data, (ip, port) = sock.recvfrom(1024)
    message = data.decode("utf-8").strip()
    print(f"Received from {ip}:{port} -> {message}")

    if message.lower() == "status":
        reply = build_report()
    else:
        reply = "Unknown command. Send 'status' to get system info."

    sock.sendto(reply.encode("utf-8"), (ip, port))
    print(f"Sent reply to {ip}:{port}")
