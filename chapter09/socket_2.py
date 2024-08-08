from socket import socket, AF_INET, SOCK_STREAM
# クライアントから接続され、受信したデータをそのまま返すサーバー
# asyncio_sample.py と同様の内容
# 実行後に別のターミナルで nc localhost 25000 と入力する
def echo_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(1)
    while True:
        client, addr = sock.accept()
        echo_handler(client, addr)

def echo_handler(client, addr):
    print(f"Connection from {addr}")
    with client:
        while True:
            data = client.recv(10_000)
            if not data:
                break
            client.sendall(data)
    print(f"Connection closed")

if __name__ == "__main__":
    echo_server(("", 25_000))
