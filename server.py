import socket 
import threading

# Configurari de baza 
IP = '127.0.0.1'
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()
print(f'Serverul a pornit pe {IP}:{PORT}')

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                raise Exception()

            decoded_message = message.decode('utf-8')

            # --- LOGICA DE COMENZI ---
            if ": " in decoded_message:
                parts = decoded_message.split(": ", 1)
                user_text = parts[1]

                if user_text == '/exit':
                    raise Exception()
                
                if user_text == '/online':
                    lista_useri = ", ".join(nicknames)
                    raspuns = f"[SERVER] Utilizatori online: {lista_useri}"
                    client.send(raspuns.encode('utf-8'))
                    continue # Nu trimitem comanda celorlalti

            # Daca nu e comanda, trimitem mesajul normal
            broadcast(message)

        except:
            # Curatenie la deconectare
            if client in clients:
                index = clients.index(client)
                nickname = nicknames[index]
                
                clients.remove(client)
                nicknames.remove(nickname)
                client.close()
                
                broadcast(f'{nickname} a parasit chatul!'.encode('utf-8'))
            break

def receive():
    print('Serverul este gata sa primeasca conexiuni...')
    while True:
        client, adress = server.accept()
        print(f'Conexiune stabilita cu {str(adress)}')

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        # SINCRONIZARE: Intai adaugam in liste, apoi anuntam
        nicknames.append(nickname)
        clients.append(client)

        broadcast(f'{nickname} a intrat in chat!'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()