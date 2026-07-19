# Multiplayer Grid Game 🎮

[中文版本](README_zh.md)

A simple 2D multiplayer grid-based game built with Python, Pygame, and TCP networking.

## ✨ Features

- 🔗 **Multiplayer Support**: Connect multiple clients to a central server for real-time gameplay
- 🔄 **Real-time State Sync**: Player positions are synchronized across all connected clients
- 📡 **TCP Networking**: Reliable communication using TCP sockets with JSON message protocol
- 🗺️ **Grid-based World**: 2D tile-based map with walls and collision detection
- 🐳 **Docker Ready**: Containerized server deployment for easy hosting
- 🌍 **Cross-platform**: Server runs on Linux, clients run on Windows/Linux

## 🚀 Getting Started

### 📋 Prerequisites

- Python 3.8+
- Pygame (for clients)
- Docker (for containerized deployment, optional)

### 💾 Installation

```bash
# Clone the repository
git clone https://github.com/weilu-a/LinuxFinal.git
cd LinuxFinal

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate.bat  # Windows

# Install dependencies (client only)
pip install pygame
```

### ▶️ Running the Game

#### 🖥️ Server

```bash
# Start server directly
python server/main.py

# Or use Docker
docker-compose up -d
```

#### 🎯 Client

```bash
# Connect to local server
python client/game.py

# Connect to remote server (modify constants.py)
# SERVER_HOST = 'your-server-ip'
```

## 🎮 Controls

- **WASD**: Move player
- **ESC**: Exit game

## 📁 Project Structure

```
LinuxFinal/
├── client/           # Game client
│   ├── game.py       # Main game loop
│   ├── player.py     # Player class
│   ├── network.py    # TCP client
│   ├── input_handler.py  # Input processing
│   └── constants.py  # Game constants
├── server/           # Game server
│   ├── main.py       # Server entry point
│   ├── game_server.py    # TCP server logic
│   ├── player_manager.py # Player state management
│   └── protocol.py   # Message protocol
├── engine/           # Game engine
│   ├── grid_world.py # Grid-based world
│   └── camera.py     # Static camera
├── data/             # Game data
│   └── maps/         # Map files
└── docker-compose.yml # Docker deployment
```

## 🔌 Network Protocol

The game uses a JSON-based message protocol over TCP:

- `JOIN`: Player joins the game
- `LEAVE`: Player leaves the game
- `MOVE`: Player position update
- `SYNC`: Full state synchronization

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## 📄 License

This project is open source for learning purposes.
