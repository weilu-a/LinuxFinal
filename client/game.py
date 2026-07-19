import pygame
import sys
import uuid
import os
from typing import Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine import GridWorld, Camera
from constants import *
from player import Player
from input_handler import InputHandler
from network import NetworkClient

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Multiplayer Game")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        map_path = os.path.join(project_root, 'data', 'maps', 'default.map')
        self.grid_world = GridWorld(map_path, TILE_SIZE)
        world_width, world_height = self.grid_world.get_world_size()
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, world_width, world_height)
        
        self.input_handler = InputHandler()
        
        self.local_player_id = str(uuid.uuid4())[:8]
        self.local_player = Player(self.local_player_id, 64, 64, (0, 255, 0), is_local=True)
        
        self.players: Dict[str, Player] = {}
        self.players[self.local_player_id] = self.local_player
        
        self.network = NetworkClient(SERVER_HOST, SERVER_PORT)
        self.connect_to_server()
        
        self.player_colors = [
            (255, 0, 0),
            (0, 0, 255),
            (255, 255, 0),
            (255, 0, 255),
            (0, 255, 255),
        ]
        self.color_index = 0

    def connect_to_server(self):
        if self.network.connect():
            join_message = {
                'type': 'join',
                'player_id': self.local_player_id,
                'name': 'Player'
            }
            self.network.send_message(join_message)
            print("Connected to server")
        else:
            print("Failed to connect to server")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def is_position_valid(self, x, y):
        player_radius = self.local_player.size / 2
        test_points = [
            (x - player_radius, y - player_radius),
            (x + player_radius, y - player_radius),
            (x - player_radius, y + player_radius),
            (x + player_radius, y + player_radius),
            (x, y),
        ]
        for px, py in test_points:
            tile_x = int(px / TILE_SIZE)
            tile_y = int(py / TILE_SIZE)
            if self.grid_world.is_wall(tile_x, tile_y):
                return False
        return True

    def update(self, delta_time):
        if pygame.key.get_focused():
            keys = pygame.key.get_pressed()
            dx, dy = self.input_handler.get_movement_vector(keys)
        else:
            dx, dy = 0, 0
        
        new_x = self.local_player.x + dx * PLAYER_SPEED * delta_time
        new_y = self.local_player.y + dy * PLAYER_SPEED * delta_time
        
        if self.is_position_valid(new_x, self.local_player.y):
            self.local_player.x = new_x
        if self.is_position_valid(self.local_player.x, new_y):
            self.local_player.y = new_y
        
        if self.network.connected:
            move_message = {
                'type': 'move',
                'player_id': self.local_player_id,
                'x': self.local_player.x,
                'y': self.local_player.y
            }
            self.network.send_message(move_message)
        
        self.process_network_messages()

    def process_network_messages(self):
        messages = self.network.get_messages()
        for msg in messages:
            msg_type = msg.get('type')
            if msg_type == 'join':
                player_id = msg.get('player_id')
                if player_id != self.local_player_id and player_id not in self.players:
                    color = self.player_colors[self.color_index % len(self.player_colors)]
                    self.color_index += 1
                    self.players[player_id] = Player(player_id, 100, 100, color, is_local=False)
            elif msg_type == 'leave':
                player_id = msg.get('player_id')
                if player_id in self.players:
                    del self.players[player_id]
            elif msg_type == 'move':
                player_id = msg.get('player_id')
                if player_id != self.local_player_id and player_id in self.players:
                    self.players[player_id].x = msg.get('x', 100)
                    self.players[player_id].y = msg.get('y', 100)
            elif msg_type == 'sync':
                players_data = msg.get('players', {})
                for player_id, data in players_data.items():
                    if player_id != self.local_player_id:
                        if player_id not in self.players:
                            color = self.player_colors[self.color_index % len(self.player_colors)]
                            self.color_index += 1
                            self.players[player_id] = Player(player_id, data['x'], data['y'], color, is_local=False)
                        else:
                            self.players[player_id].x = data['x']
                            self.players[player_id].y = data['y']

    def render(self):
        self.screen.fill((30, 30, 30))
        
        self.grid_world.render(self.screen, self.camera)
        
        for player in self.players.values():
            player.draw(self.screen, self.camera)
        
        pygame.display.flip()

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60) / 1000.0
            
            self.handle_events()
            self.update(delta_time)
            self.render()
        
        if self.network.connected:
            leave_message = {
                'type': 'leave',
                'player_id': self.local_player_id
            }
            self.network.send_message(leave_message)
            self.network.disconnect()
        
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()
