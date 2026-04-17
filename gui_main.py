import customtkinter as ctk
from database import DataBaseManager
import socket
import threading
import json

# Setările de temă
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.db = DataBaseManager()
        
        self.title("Smart Sentinel - Login")
        self.geometry("400x500")

        self.label = ctk.CTkLabel(self, text="Welcome Back", font=("Inter", 24, "bold"))
        self.label.pack(pady=40)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username", width=250, height=40)
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=250, height=40)
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login_event, width=250, height=40)
        self.login_button.pack(pady=20)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red", font=("Inter", 12))
        self.error_label.pack(pady=5)
    
    def login_event(self):
        user = self.username_entry.get()
        pw = self.password_entry.get()
        user_id = self.db.verify_user(user, pw)
    
        if user_id:
            self.error_label.configure(text="Login successful!", text_color="green")
            self.open_chat_dashboard(user_id)
        else:
            self.error_label.configure(text="Invalid username or password", text_color="red")
    
    def open_chat_dashboard(self, user_id):
        self.dashboard = ChatDashboard(user_id)
        self.withdraw()

class ChatDashboard(ctk.CTkToplevel):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.db = DataBaseManager()
        self.current_peer_id = None
        
        self.title("Smart Sentinel - Dashboard")
        self.geometry("900x600")
        
        # 1. Configurare Socket Client
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(('127.0.0.1', 55555))
            self.client_socket.send(str(self.user_id).encode('utf-8'))
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except:
            print("Serverul este offline. Mod Offline activat.")

        # Grid Sistem
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # SIDEBAR
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="CHATS", font=("Inter", 20, "bold"))
        self.logo_label.pack(pady=20)

        self.users_list_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.users_list_frame.pack(fill="both", expand=True)

        self.load_users()

        # CHAT AREA
        self.chat_frame = ctk.CTkFrame(self, corner_radius=15)
        self.chat_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.chat_label = ctk.CTkLabel(self.chat_frame, text="Select a chat to start", font=("Inter", 16, "italic"))
        self.chat_label.pack(pady=10)

        self.textbox = ctk.CTkTextbox(self.chat_frame, state="disabled", font=("Inter", 13))
        self.textbox.pack(padx=20, pady=(10, 10), fill="both", expand=True)

        self.msg_entry = ctk.CTkEntry(self.chat_frame, placeholder_text="Type a message...", height=40)
        self.msg_entry.pack(padx=20, pady=20, fill="x")
        self.msg_entry.bind("<Return>", lambda event: self.send_message())

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_users(self):
        for child in self.users_list_frame.winfo_children():
            child.destroy()
            
        users = self.db.get_all_users(self.user_id)
        for u_id, u_name in users:
            btn = ctk.CTkButton(
                self.users_list_frame, 
                text=u_name, 
                fg_color="transparent",
                anchor="w",
                command=lambda i=u_id, n=u_name: self.select_chat(i, n)
            )
            btn.pack(fill="x", padx=10, pady=2)

    def select_chat(self, peer_id, peer_name):
        self.current_peer_id = peer_id
        self.current_peer_name = peer_name
        self.chat_label.configure(text=f"Chatting with: {peer_name}", font=("Inter", 16, "bold"))
        self.update_chat_display()

    def update_chat_display(self):
        if self.current_peer_id is None:
            return
        
        messages = self.db.get_chat_history(self.user_id, self.current_peer_id)
        
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        
        self.textbox.tag_config("me", foreground="#1f538d")
        self.textbox.tag_config("peer", foreground="#AAB7B8") 

        for msg in messages:
            if len(msg) == 3:
                sender_id, content, timestamp = msg
            else:
                sender_id, content, timestamp = None, msg[0], msg[1]

            time_short = timestamp[11:16]
            
            if sender_id == self.user_id:
                self.textbox.insert("end", f"[{time_short}] Me: ", "me")
                self.textbox.insert("end", f"{content}\n")
            else:
                name = getattr(self, 'current_peer_name', 'Friend')
                self.textbox.insert("end", f"[{time_short}] {name}: ", "peer")
                self.textbox.insert("end", f"{content}\n")
        
        self.textbox.configure(state="disabled")
        self.textbox.see("end")

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                if not data: break
                
                msg_data = json.loads(data)
                self.db.save_message(
                    sender_id=msg_data['sender_id'],
                    receiver_id=self.user_id,
                    content=msg_data['content'],
                    is_group=msg_data['is_group']
                )
                
                if self.current_peer_id == msg_data['sender_id']:
                    self.update_chat_display()
            except: break

    def send_message(self):
        content = self.msg_entry.get()
        if content and self.current_peer_id:
            self.db.save_message(self.user_id, self.current_peer_id, content, is_group=False)
            
            message_packet = {
                "sender_id": self.user_id,
                "receiver_id": self.current_peer_id,
                "content": content,
                "is_group": False
            }
            
            try:
                self.client_socket.send(json.dumps(message_packet).encode('utf-8'))
            except:
                print("Eroare la trimitere prin rețea.")

            self.msg_entry.delete(0, "end")
            self.update_chat_display()

    def on_closing(self):
        self.client_socket.close()
        self.destroy()
        exit()

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()