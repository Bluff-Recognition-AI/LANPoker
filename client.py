import sys
import time
import json
from libs.gameui.gameui.game import Game, State
from libs.web.socketserverclient.json_client import JSONClient
from log import Log

SCREEN_SIZE = (800, 600)
NAME = "Szymon"

BUTTON_MOVE_MAP = {"Call": "CALL", "Raise": "RAISE", "Fold": "FOLD"}
LOG_FILE_PREFIX = "client_log_"
LOG_FILE_EXTENSION = ".json"


class Client:
    def __init__(self, host_ip, host_port):
        self.host_ip = host_ip
        self.host_port = host_port
        self.game = Game()

        self.player_id = None
        self.web_client = JSONClient(host_ip, host_port)
        self.web_client.connect()
        self.web_client.send_data({"name": NAME})

        self.log = Log(LOG_FILE_PREFIX + str(time.time()) + LOG_FILE_EXTENSION)

        while True:
            data = self.web_client.get_data()
            if data:
                if "player_id" in data:
                    self.player_id = data["player_id"]
                    break

        self.game.focus_player = self.player_id
        print("connected")

    def close(self):
        self.log.save()
        self.game.close()
        print("closed game")
        self.web_client.close()
        print("closed web client")
        # sys.exit()

    def make_move(self, name, value=None):
        self.web_client.send_data({"name": name, "value": value})
        data = {"timestamp": time.time(), "move": name, "value": value, "bluff": "?"}
        self.log.write(data)
        self.log.save()

    def run(self):

        while self.game.running:
            try:
                data = self.web_client.get_data()
                if data:
                    self.game.load_gamestate(data)

                action = self.game.step()
                if action:
                    print(f"\nbluff {self.game.bluff}  :   action {self.game.action}\n")
                    if action == "Raise":
                        self.make_move(BUTTON_MOVE_MAP[action], self.game.bet)
                    elif action in BUTTON_MOVE_MAP:
                        self.make_move(BUTTON_MOVE_MAP[action])
            except:
                break

        self.close()


def test():
    ip = sys.argv[1]
    client = Client(ip, 5554)
    client.run()


if __name__ == "__main__":
    test()
