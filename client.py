import sys
from libs.gameui.gameui.game import Game
from libs.web.socketserverclient.json_client import JSONClient

SCREEN_SIZE = (800, 600)
NAME = "Szymon"

class Client:
    def __init__(self, host_ip, host_port):
        self.host_ip = host_ip
        self.host_port = host_port
        self.game = Game()

        self.player_id = None
        self.web_client = JSONClient(host_ip, host_port)
        self.web_client.connect()
        self.web_client.send_data({"name": NAME})
        
        while(True):
            data = self.web_client.get_data()
            if(data):
                if("player_id" in data):
                    self.player_id = data["player_id"]
                    break
        
        self.game.focus_player = self.player_id
        print("connected")

    def run(self):

        while(self.game.running):
            data = self.web_client.get_data()
            if data:
                self.game.load_gamestate(data)

            action = self.game.step()
            if action:
                if action == "Call":
                    self.web_client.send_data({"name": "CALL", "value": None})
                elif action == "Fold":
                    self.web_client.send_data({"name": "FOLD", "value": None})

        self.web_client.close()

def test():
    ip = sys.argv[1]
    client = Client(ip, 5555)
    client.run()

if __name__ == "__main__":
    test()