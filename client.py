import socket
import threading
import sys

# 1. Introducere date
nickname = input("Alege un nickname: ")
if not nickname:
    nickname = "Guest"

# 2. Configurare Conexiune
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(('127.0.0.1', 55555))
except ConnectionRefusedError:
    print("Serverul nu este pornit!")
    sys.exit()

# 3. Funcția de ascultare (Server -> Client)
def receive():
    while True:
        try:
            # Primeste mesajul de la server
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                # Folosim un print curat
                print(f"\r{message}\n> ", end="") 
        except:
            print("\nConexiunea cu serverul a fost pierdută!")
            client.close()
            break

# 4. Funcția de trimitere (Client -> Server)
def write():
    while True:
        try:
            # Citim mesajul de la utilizator
            user_input = input("> ")
            message = f'{nickname}: {user_input}'
            client.send(message.encode('utf-8'))
            
            # Daca utilizatorul a scris /exit, inchidem si clientul local
            if user_input == '/exit':
                client.close()
                break
        except EOFError:
            break
        except:
            print("Eroare la trimiterea mesajului!")
            client.close()
            break

# 5. Pornirea thread-urilor
receive_thread = threading.Thread(target=receive)
receive_thread.daemon = True # Thread-ul se inchide automat cand se inchide programul
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()