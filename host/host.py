from libs.web import json_server as s
from libs.engine import engine

import time
import json
import threading


# game setup
config = s.PokerConfig(500, 1000, 2000, 3)
players = [engine.Player("Ricky", 10000), s.Player("Julian", 10000), s.Player("John", 10000)]

engine = engine.PokerEngine()
engine.set_config(config)

for player in players:
    engine.add_player(player)

engine.reset()
engine.game_step()

# server setup
HOST = '0.0.0.0'  # All available interfaces
PORT = 5555  # Arbitrary port number
server = s.JSONServer(HOST, PORT)
server_thread = threading.Thread(target=server.start)
server_thread.start()

input("if all the players connected press any button")

while(engine.running):
    if(engine.game_phase != engine.GamePhase.WAITING_MOVE):
        engine.game_step()
    else:
        print(engine.get_game_state())
        server.broadcast(json.dumps("Input move:"))
        # move_name = input()
        while not server.client_data:
            time.sleep(0.2)
        move_name = json.loads(server.client_data[0])
        print(move_name)
        server.client_data.clear()

        value = None
        if(move_name == engine.MoveType.BET.value or move_name == engine.MoveType.RAISE.value):
            server.broadcast(json.dumps("Input value: (min 4000)"))
            # value = int(input())
            while not server.client_data:
                time.sleep(0.2)
            value = json.loads(server.client_data[0])
            server.client_data.clear()
        if value:
            value = int(value)
        move = engine.Move(engine.MoveType(move_name), value)
        print(vars(move))
        engine.game_step(move)

    print(engine.get_game_state())