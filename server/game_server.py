import socket
import json
import threading
from typing import Dict

from protocol import *
from player_manager import PlayerManager

class GameServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.player_manager = PlayerManager()

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        
        print(f"Server started on {self.host}:{self.port}")
        
        accept_thread = threading.Thread(target=self._accept_loop, daemon=True)
        accept_thread.start()

    def _accept_loop(self):
        while self.running:
            try:
                conn, addr = self.server_socket.accept()
                print(f"New connection from {addr}")
                
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(conn, addr),
                    daemon=True
                )
                client_thread.start()
            except Exception:
                if self.running:
                    print("Error accepting connection")

    def _handle_client(self, conn, addr):
        buffer = ""
        player_id = None
        
        try:
            while self.running:
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break
                
                buffer += data
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    try:
                        message = json.loads(line)
                        player_id = self._process_message(message, conn)
                    except json.JSONDecodeError:
                        pass
        except Exception as e:
            print(f"Client {addr} error: {e}")
        finally:
            if player_id:
                self._handle_player_leave(player_id, conn)
            try:
                conn.close()
            except:
                pass
            print(f"Client {addr} disconnected")

    def _process_message(self, message: Dict, conn) -> str:
        msg_type = message.get('type')
        player_id = message.get('player_id')
        
        if msg_type == 'join':
            return self._handle_player_join(player_id, conn)
        elif msg_type == 'leave':
            self._handle_player_leave(player_id, conn)
        elif msg_type == 'move':
            x = message.get('x', 0.0)
            y = message.get('y', 0.0)
            self._handle_player_move(player_id, x, y)
        
        return player_id

    def _handle_player_join(self, player_id: str, conn):
        self.player_manager.add_player(player_id, conn)
        
        sync_msg = create_sync_message(self.player_manager.get_all_players())
        self._send_to(conn, sync_msg)
        
        join_msg = create_join_message(player_id)
        self._broadcast(join_msg, exclude=conn)
        
        print(f"Player {player_id} joined")
        return player_id

    def _handle_player_leave(self, player_id: str, conn):
        self.player_manager.remove_player(player_id)
        
        leave_msg = create_leave_message(player_id)
        self._broadcast(leave_msg)
        
        print(f"Player {player_id} left")

    def _handle_player_move(self, player_id: str, x: float, y: float):
        self.player_manager.update_player_position(player_id, x, y)
        
        move_msg = create_move_message(player_id, x, y)
        self._broadcast(move_msg)

    def _send_to(self, conn, message: Dict):
        try:
            data = json.dumps(message) + '\n'
            conn.sendall(data.encode('utf-8'))
        except Exception as e:
            print(f"Send failed: {e}")

    def _broadcast(self, message: Dict, exclude=None):
        for conn in self.player_manager.get_all_connections():
            if conn != exclude:
                self._send_to(conn, message)

    def stop(self):
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        print("Server stopped")
