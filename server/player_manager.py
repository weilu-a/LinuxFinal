from typing import Dict, Tuple

class PlayerManager:
    def __init__(self):
        self.players: Dict[str, dict] = {}
        self.connections: Dict[str, object] = {}

    def add_player(self, player_id: str, connection):
        self.players[player_id] = {
            'x': 100.0,
            'y': 100.0,
            'name': 'Player'
        }
        self.connections[player_id] = connection

    def remove_player(self, player_id: str):
        if player_id in self.players:
            del self.players[player_id]
        if player_id in self.connections:
            del self.connections[player_id]

    def update_player_position(self, player_id: str, x: float, y: float):
        if player_id in self.players:
            self.players[player_id]['x'] = x
            self.players[player_id]['y'] = y

    def get_player(self, player_id: str):
        return self.players.get(player_id)

    def get_all_players(self):
        return dict(self.players)

    def get_connection(self, player_id: str):
        return self.connections.get(player_id)

    def get_all_connections(self):
        return list(self.connections.values())

    def get_player_count(self):
        return len(self.players)
