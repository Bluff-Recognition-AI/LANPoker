import sys
import time
import json
from new_record_video import *
from libs.gameui.gameui.game import Game
from libs.web.socketserverclient.json_client import JSONClient
from log import Log

SCREEN_SIZE = (800, 600)

BUTTON_MOVE_MAP = {
    "Call": "CALL",
    "Raise": "RAISE",
    "Fold": "FOLD"
}
LOG_FILE_PREFIX = "client_log_"
LOG_FILE_EXTENSION = ".json"

class Client:
    def __init__(self, host_ip, host_port, name):
        self.host_ip = host_ip
        self.host_port = host_port
        self.name = name
        self.game = Game()
        self.recorder = Recorder()
        self.recorder.start(5)

        self.player_id = None
        self.web_client = JSONClient(host_ip, host_port)
        self.web_client.connect()
        self.web_client.send_data({"name": self.name})

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
        self.recorder.close()
        print("closed camera thread")

    def make_move(self, action):
        data = action
        data["timestamp"] = time.time()
        self.web_client.send_data(data)
        self.log.write(data)
        self.log.save()

    def run(self):
        while self.game.running:
            data = self.web_client.get_data()
            if data:
                self.game.load_gamestate(data)
            action = self.game.step()
            if action:
                self.make_move(action)
                if action["bluff"]:
                    self.recorder.record(action["timestamps"][0])
                    if hasattr(self.recorder, "camera_thread"):
                        self.recorder.camera_thread.join()
                    self.recorder.save_the_file(action["name"], action["bluff"], self.name)
                    self.recorder.start_recording = False
                    self.recorder.start(5)

        self.close()


def main():
    name = sys.argv[1]
    ip = sys.argv[2]
    client = Client(ip, 5554, name)
    client.run()

if __name__ == "__main__":
    main()
