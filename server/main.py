"""Game Server Main Entry Point

This module starts the TCP game server that handles multiplayer game sessions.
"""

import time
import sys
import os
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game_server import GameServer


def main(host: str = '0.0.0.0', port: int = 5555) -> None:
    """Start the game server.
    
    Args:
        host: The host address to bind to. Defaults to '0.0.0.0' (all interfaces).
        port: The port number to listen on. Defaults to 5555.
    """
    server: Optional[GameServer] = None
    try:
        server = GameServer(host, port)
        server.start()
        
        print(f"Server running on {host}:{port}. Press Ctrl+C to stop.")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping server...")
        if server:
            server.stop()
        sys.exit(0)
    except Exception as e:
        print(f"Server error: {e}")
        if server:
            server.stop()
        sys.exit(1)


if __name__ == '__main__':
    main()
