from socket import socket, AF_INET, SOCK_DGRAM

def run_server(address):
    sock = socket(AF_INET, SOCK_DGRAM)  # UDP ソケットを作成
    sock.bind(address)  # アドレスとポートにバインド
    while True:
        _, addr = sock.recvfrom(2_000)  # メッセージを受信
        response = b"world"
        sock.sendto(response, addr)  # レスポンスを送信

def run_client(address):
    sock = socket(AF_INET, SOCK_DGRAM)  # UDP ソケットを作成
    sock.sendto(b"hello", address)  # メッセージを送信
    response, _ = sock.recvfrom(2_000)  # レスポンスを受信
    print("received:", response)
    sock.close()

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        raise SystemExit(f"Usage: {sys.argv[0]} [-server|-client] host port")
    address = (sys.argv[2], int(sys.argv[3]))
    if sys.argv[1] == "-server":
        run_server(address)
    if sys.argv[1] == "-client":
        run_client(address)
