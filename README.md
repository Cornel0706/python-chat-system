# 💬 Python Multi-User Chat System

A real-time messaging system based on the **Client-Server architecture**, built using the **TCP/IP** protocol. This project demonstrates the practical application of **Multithreading** to handle concurrent connections and low-level networking via Python's `socket` library.

## 🚀 Features v0.1

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

## 🚀 Key Features (v2.0)

* **Ultra-Modern GUI**: Built with `CustomTkinter`, featuring a native Dark Mode design, rounded corners, and a fluid user experience.
* **Persistent Database**: Full integration with **SQLite** to store message history, user accounts, and group structures.
* **Security First**: Authentication system using passwords protected by the **SHA-256** hashing algorithm (passwords are never stored in plain text).
* **Smart Routing**: The server processes **JSON** data packets to deliver messages directly to the correct `receiver_id`.
* **Dynamic Sidebar**: An automated contact list that populates and updates directly from the database.

---

## 🛠️ Tech Stack

* **Language**: Python 3.12
* **Graphical Interface**: CustomTkinter / Pillow (for images/icons)
* **Database**: SQLite3
* **Networking**: Socket / Threading / JSON
* **Security**: Hashlib (SHA-256)

---

## 🏗️ System Architecture

The system operates on a **Client-Server-Database** architecture:
1. **Server**: Acts as an intelligent dispatcher, managing active connections in a dictionary format: `{user_id: socket}`.
2. **Client (GUI)**: Handles user interaction, displays chat history, and sends structured JSON packets to the server.
3. **Database**: Maintains data integrity (Messages, Users, Group Members) and allows for offline history viewing.

---