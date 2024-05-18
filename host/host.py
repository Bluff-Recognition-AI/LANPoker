from engine import *
from player import *
from json_server import *
import threading

PLAYER_COUNT = 4


def init_engine(players: list) -> PokerEngine:
    config = PokerConfig(500, 1000, 2000, PLAYER_COUNT)
    engine = PokerEngine()
    engine.set_config(config)

    for player in players:
        engine.add_player(player)

    engine.reset()
    engine.game_step()
    return engine

def init_server() -> JSONServer:
    HOST = '0.0.0.0'  # All available interfaces
    PORT = 5555  # Arbitrary port number
    server = JSONServer(HOST, PORT)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()
    return server

def main():
    players = [Player("Marcin", 10000), Player("Szymon", 10000), Player("Julia", 10000), Player("Wiktor", 10000)]
    engine = init_engine(players)
    
    server = init_server()

    print("wait for the players to connect")
    while len(server.clients) != PLAYER_COUNT:
        time.sleep(0.1)
    
    player_connection = {}
    for i in range(PLAYER_COUNT):
        server.send_to([players[i].name, i], server.clients[i])     # sends to each player his name and client info
        player_connection[players[i]] = server.clients[i]           
 
    server.broadcast("\nGAME STARTS\n")
    time.sleep(1)
    while(engine.running):
        if(engine.game_phase != GamePhase.WAITING_MOVE):
            engine.game_step()
        else:
            info = engine.get_game_state() 
            for key in info:
                print(f"{key} : {info[key]}")
            server.broadcast({"gamestate": info})
            server.send_to("Input move:", player_connection[players[engine.get_game_state()["turn"]]])
            move_name = server.wait_data()

            value = None
            if(move_name == MoveType.BET.value or move_name == MoveType.RAISE.value):
                server.send_to("Input value: (min 4000)", player_connection[players[engine.get_game_state()["turn"]]])
                value = server.wait_data()
            if value:
                value = int(value)
            move = Move(MoveType(move_name), value)
            print(vars(move))
            server.broadcast({"playermove": [move_name, value]})

            engine.game_step(move)


        info = engine.get_game_state() 
        for key in info:
            print(f"{key} : {info[key]}")
        server.broadcast({"gamestate": info})
        time.sleep(1)
    

if __name__ == "__main__":
    main()