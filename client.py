import threading
import pygame
from libs.gameui.gameui.game import Game
from libs.web.socketserverclient.json_client import JSONClient

tmp = {
    "config": {
        "ante": 500,
        "small_blind": 1000,
        "big_blind": 2000,
        "player_count": 6
    },
    "players": [
        {
            "name": "Szymon",
            "money": 9500
        },
        {
            "name": "Karol",
            "money": 9500
        },
        {
            "name": "Jezy",
            "money": 9500
        },
        {
            "name": "Julia",
            "money": 1000
        },
        {
            "name": "Kasia",
            "money": 20200
        },
        {
            "name": "Kasia",
            "money": 20200
        }
    ],
    "phase": "WAITING_MOVE",
    "turn": 2,
    "hands": [
        [
            "c9",
            "s5"
        ],
        [
            "c7",
            "d9"
        ],
        [
            "c5",
            "s6"
        ],
        [
            "c5",
            "s6"
        ],
        [
            "c5",
            "s6"
        ],
        [
            "c5",
            "s6"
        ]
    ],
    "board": ["cK", "sA"],
    "stacks": [
        8500,
        7500,
        9500,
        1000,
        20200,
        20200
    ],
    "bets": [
        1000,
        2000,
        0,
        0,
        0,
        0
    ]
}

SCREEN_SIZE = (800, 600)
NAME = "Szymon"

class Client:
    def __init__(self, host_ip, host_port):
        self.host_ip = host_ip
        self.host_port = host_port
        self.game = Game()
        #self.game.load_gamestate(tmp)

        self.web_client = JSONClient(host_ip, host_port)
        self.web_client.connect()
        self.web_client.send_data({"name": NAME})
        print("connected")

    def run(self):

        while(self.game.running):
            data = self.web_client.get_data()
            #data = tmp
            if data:
                self.game.load_gamestate(data)

            self.game.step()

def test():

    client = Client("10.128.130.160", 5555)
    client.run()

if __name__ == "__main__":
    test()