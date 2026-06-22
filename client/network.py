import socket
import json
import threading
import queue
from typing import Dict, Any

class NetworkClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self.receive_thread = None
        self.message_queue = queue.Queue()
        self.lock = threading.Lock()

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
            self.receive_thread.start()
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def _receive_loop(self):
        buffer = ""
        while self.connected:
            try:
                data = self.socket.recv(1024).decode('utf-8')
                if not data:
                    self.disconnect()
                    break
                buffer += data
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    try:
                        message = json.loads(line)
                        self.message_queue.put(message)
                    except json.JSONDecodeError:
                        pass
            except Exception:
                self.disconnect()
                break

    def send_message(self, message: Dict[str, Any]):
        if not self.connected or not self.socket:
            return
        try:
            data = json.dumps(message) + '\n'
            self.socket.sendall(data.encode('utf-8'))
        except Exception as e:
            print(f"Send failed: {e}")
            self.disconnect()

    def get_messages(self):
        messages = []
        while not self.message_queue.empty():
            messages.append(self.message_queue.get())
        return messages

    def disconnect(self):
        self.connected = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
