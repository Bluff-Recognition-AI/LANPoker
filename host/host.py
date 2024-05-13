from libs.web import json_server as s
from libs.engine import engine as eng
from libs.engine import player


import threading


def main():
    # game setup
    config = eng.PokerConfig(500, 1000, 2000, 3)
    players = [player.Player("Ricky", 10000), player.Player("Julian", 10000), player.Player("John", 10000)]

    engine = eng.PokerEngine()
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
        if(engine.game_phase != eng.GamePhase.WAITING_MOVE):
            engine.game_step()
        else:
            print(engine.get_game_state())
            server.broadcast("Input move:")
            # move_name = input()
            move_name = server.wait_data()
            print(move_name)

            value = None
            if(move_name == eng.MoveType.BET.value or move_name == eng.MoveType.RAISE.value):
                server.broadcast("Input value: (min 4000)")
                # value = int(input())
                value = server.wait_data()
            if value:
                value = int(value)
            move = eng.Move(eng.MoveType(move_name), value)
            print(vars(move))
            engine.game_step(move)

        print(engine.get_game_state())

if __name__ == "__main__":
    main()