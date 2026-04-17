import socket
import threading
import json

# Configurari
IP = '127.0.0.1'
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()

# Dicționar pentru a stoca {user_id: client_socket}
online_clients = {}

def handle_client(client_socket, user_id):
    print(f"[SERVER] Utilizatorul {user_id} s-a conectat.")
    
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            
            message_packet = json.loads(data)
            receiver_id = message_packet.get("receiver_id")
            
            if receiver_id in online_clients:
                target_socket = online_clients[receiver_id]
                target_socket.send(json.dumps(message_packet).encode('utf-8'))
                print(f"[SERVER] Mesaj de la {user_id} către {receiver_id}")
            else:
                print(f"[SERVER] Destinatarul {receiver_id} este offline. Mesajul rămâne doar în DB.")
                
        except:
            break

    # Curatenie la deconectare
    if user_id in online_clients:
        del online_clients[user_id]
    client_socket.close()
    print(f"[SERVER] Utilizatorul {user_id} s-a deconectat.")

def receive():
    print(f"Serverul rulează pe {IP}:{PORT}...")
    while True:
        client, address = server.accept()

        try:
            user_id = int(client.recv(1024).decode('utf-8'))
            online_clients[user_id] = client
            
            thread = threading.Thread(target=handle_client, args=(client, user_id))
            thread.start()
        except:
            client.close()

if __name__ == "__main__":
    receive()