# コードを実行した後に nc localhost 25000 で接続して文字列を送信する
import asyncio
import socket

async def echo_server(address):
    loop = asyncio.get_event_loop()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    sock.setblocking(False)
    print("server listening at", address)
    with sock:
        while True:
            client, addr = await loop.sock_accept(sock)
            print("connection from", addr)
            loop.create_task(echo_client(loop, client))

async def echo_client(loop, client):
    with client:
        while True:
            data = await loop.sock_recv(client, 10000)
            if not data:
                break
            await loop.sock_sendall(client, b"got:" + data)
    print("connection closed")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(echo_server(("localhost", 25000)))
    loop.run_forever()
