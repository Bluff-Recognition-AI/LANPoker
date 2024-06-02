from libs.engine.pokerengine.engine import *
from libs.engine.pokerengine.player import *
from libs.web.socketserverclient.json_server import *
import threading

HOST = '0.0.0.0'  # All available interfaces
PORT = 5554  # Arbitrary port number

PLAYER_COUNT = 2
ANTE = 0
SMALL_BLIND = 100
BIG_BLIND = 200
START_MONEY = 10000

CONFIG = PokerConfig(ANTE, SMALL_BLIND, BIG_BLIND, PLAYER_COUNT)

class Host:
    def __init__(self):
        self.engine = PokerEngine(CONFIG)
        self.server = JSONServer(HOST, PORT)
        self.players = []
        self.running = False

    def start_server(self):
        self.server_thread = threading.Thread(target=self.server.start)
        self.server_thread.start()

    def start_engine(self):
        for player in self.players:
            self.engine.add_player(player)

        self.engine.reset()
        self.server.broadcast(self.engine.get_game_state())

    def game_init(self):
        self.start_server()
        print("wait for the players to connect")
        self.players = []
        while len(self.server.clients) != PLAYER_COUNT:
            data = self.server.wait_data()
            if "name" in data:
                self.players.append(Player(data["name"], START_MONEY))
                player_id = len(self.server.clients) - 1
                self.server.send_to({"player_id": player_id}, self.server.clients[player_id])

                print(f"{(data['name'])} joined the game! ({len(self.players)}/{self.engine.config.player_count})")
            time.sleep(0.1)

        self.start_engine()

    def play_one_hand(self):
        while self.engine.running:
            if self.engine.game_phase != GamePhase.WAITING_MOVE:
                self.engine.game_step()
            else:
                move_get = self.server.wait_data()
                move = Move(MoveType(move_get["name"]), move_get["value"])
                print(vars(move))

                self.engine.game_step(move)

            print(self.engine.get_game_state())
            self.server.broadcast(self.engine.get_game_state())
            time.sleep(0.5)

    def start(self):
        print("Host started!")
        self.game_init()
        time.sleep(0.1)
        self.running = True
        while(self.running):
            self.play_one_hand()
            self.engine.next_hand()
    
    def close(self):
        self.running = False
        print("Host closed!")

def main():
    host = Host()
    host.start()
    # host_thread = threading.Thread(target=host.start)
    # while(True):
    #     decision = input("Close host? (Y/n)")
    #     if decision.upper() == "Y":
    #         host.close()
    #         break

if __name__ == "__main__":
    main()
