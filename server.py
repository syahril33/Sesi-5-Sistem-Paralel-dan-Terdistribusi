import socket
import threading

HOST = '127.0.0.1'  
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []

def broadcast(message, _client=None):
    for client in clients:
        if client != _client:  
            try:
                client.send(message)
            except:
                client.close()
                remove_client(client)

def remove_client(client):
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        username = usernames[index]
        usernames.remove(username)
        print(f"{username} Keluar Dari Room.")
        broadcast(f"{username} Keluar Dari Room.".encode('utf-8'))

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if message:
                broadcast(message, client)
        except:
            remove_client(client)
            break


def receive():
    print(f"Server berjalan di {HOST}:{PORT}")
    while True:
        client, address = server.accept()
        print(f"Terhubung dengan {str(address)}")

        client.send("USERNAME".encode('utf-8'))
        username = client.recv(1024).decode('utf-8')
        usernames.append(username)
        clients.append(client)

        print(f"Username: {username}")
        broadcast(f"{username} Bergabung ke Dalam Room!".encode('utf-8'))
        client.send("Terhubung ke server!".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()