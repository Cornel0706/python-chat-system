# 💬 Python Multi-User Chat System

A real-time messaging system based on the **Client-Server architecture**, built using the **TCP/IP** protocol. This project demonstrates the practical application of **Multithreading** to handle concurrent connections and low-level networking via Python's `socket` library.

## 🚀 Features v1

* **Real-time Communication**: Messages are broadcasted instantly to all connected users.
* **Multithreaded Architecture**: The server can handle multiple clients simultaneously by spawning a dedicated thread for each connection.
* **Command System**:
    * `/online` - Displays the list of currently active users (sent only to the requester).
    * `/exit` - Safely disconnects the client and notifies the group.
* **Error Handling**: Automatic cleanup of user lists and socket closure if a client disconnects unexpectedly.
* **Handshake Protocol**: Initial "NICK" signal exchange to collect and synchronize nicknames across the network.

## 🛠️ Tech Stack

* **Language**: Python 3.x
* **Standard Modules**:
    * `socket`: For network communication at the transport layer (TCP).
    * `threading`: For parallel execution of reading and writing tasks.

## 📦 Installation and Usage

1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/your-username/python-chat-system.git](https://github.com/your-username/python-chat-system.git)
    cd python-chat-system
    ```

2.  **Start the Server**:
    Open a terminal and run:
    ```bash
    python server.py
    ```

3.  **Connect Clients**:
    Open multiple new terminals and run in each:
    ```bash
    python client.py
    ```

## 🏗️ Project Architecture

The system operates on a **Broadcast Model**:
1. The **Client** sends a packet of `bytes` to the server.
2. The **Server** intercepts the packet and checks for internal commands (like `/online`).
3. If no command is detected, the server re-transmits (broadcasts) the message to every other client in the active list.

## 📈 Roadmap

- [ ] **Private Messaging**: Implement `/msg <user> <message>` functionality.
- [ ] **GUI**: Build a graphical user interface using **Tkinter** or **PyQt**.
- [ ] **Security**: Add End-to-End Encryption (E2EE) using the `cryptography` library.
- [ ] **Persistence**: Integrate an **SQLite** database to store chat history.
