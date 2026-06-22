import time
import sys
import os

from game_server import GameServer

def main():
    host = '0.0.0.0'
    port = 5555
    
    server = GameServer(host, port)
    server.start()
    
    print("Server running. Press Ctrl+C to stop.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping server...")
        server.stop()
        sys.exit(0)

if __name__ == '__main__':
    main()
