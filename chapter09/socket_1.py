from socket import socket, AF_INET, SOCK_STREAM
# 外部にあるサーバーに接続してデータを取得する
sock = socket(AF_INET, SOCK_STREAM)
sock.connect(("python.org", 80))
sock.send(b"GET /index.html HTTP/1.0\r\n\r\n")
parts = []
while True:
    part = sock.recv(10_000)
    if not part:
        break
    parts.append(part)
parts = b"".join(parts)
print(parts)
