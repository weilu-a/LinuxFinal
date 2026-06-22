MESSAGE_TYPES = {
    'JOIN': 'join',
    'LEAVE': 'leave',
    'MOVE': 'move',
    'SYNC': 'sync',
}

def create_join_message(player_id: str, name: str = ''):
    return {
        'type': 'join',
        'player_id': player_id,
        'name': name
    }

def create_leave_message(player_id: str):
    return {
        'type': 'leave',
        'player_id': player_id
    }

def create_move_message(player_id: str, x: float, y: float):
    return {
        'type': 'move',
        'player_id': player_id,
        'x': x,
        'y': y
    }

def create_sync_message(players: dict):
    return {
        'type': 'sync',
        'players': players
    }
