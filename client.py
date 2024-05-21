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
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
        
        self.game = Game(self.screen)
        #self.game.load_gamestate(tmp)

        self.web_client = JSONClient(host_ip, host_port)
        self.web_client.connect()
        self.web_client.send_data({"name": NAME})
        print("connected")

    def run(self):

        running = True
        while(running):
            data = self.web_client.get_data()
            if data:
                self.game.load_gamestate()
            self.game.game_frame(self.screen)

def test():

    client = Client("10.1.4.118", 5555)
    client.run()

if __name__ == "__main__":
    test()