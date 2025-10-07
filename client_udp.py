#!/usr/bin/python3
import socket

IP = "10.217.66.15"   # Raspberry Pi IP
PORT = 9090

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b"status", (IP, PORT))

data, _ = sock.recvfrom(65535)  # big buffer for large report
print("=== System Info Report ===")
print(data.decode("utf-8"))
