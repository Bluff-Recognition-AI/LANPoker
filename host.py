from libs.engine.pokerengine.engine import *
from libs.engine.pokerengine.player import *
from libs.web.socketserverclient.json_server import *
import threading
import traceback

PLAYER_COUNT = 6


def init_engine(players: list) -> PokerEngine:
    config = PokerConfig(0, 500, 1000, PLAYER_COUNT)
    engine = PokerEngine(config)

    for player in players:
        engine.add_player(player)

    engine.reset()
    engine.game_step()
    return engine


def init_server() -> JSONServer:
    HOST = '0.0.0.0'  # All available interfaces
    PORT = 5554  # Arbitrary port number
    server = JSONServer(HOST, PORT)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()
    return server


def main():
    
    server = init_server()
    print("wait for the players to connect")
    players = []
    while len(server.clients) != PLAYER_COUNT:
        data = server.wait_data()
        if "name" in data:
            players.append(Player(data["name"], 10000))
            player_id = len(server.clients) - 1
            server.send_to({"player_id": player_id}, server.clients[player_id])
        time.sleep(0.1)

    engine = init_engine(players)
    server.broadcast(engine.get_game_state())

    time.sleep(0.1)
    while engine.running:
        if engine.game_phase != GamePhase.WAITING_MOVE:
            engine.game_step()
        else:
            move_get = server.wait_data()
            move = Move(MoveType(move_get["name"]), move_get["value"])
            print(vars(move))

            engine.game_step(move)

        print(engine.get_game_state())
        server.broadcast(engine.get_game_state())
        time.sleep(0.5)


if __name__ == "__main__":
    main()
