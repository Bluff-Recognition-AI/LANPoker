import threading
from libs.gameui.gameui.game import Game

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

class Client:
    def __init__(self, host_ip, host_port):
        self.host_ip = host_ip
        self.host_port = host_port
        
        
        self.game = Game(tmp)

    def run(self):
        self.game.run()

def test():
    client = Client("198.111.111.111", "4200")
    client.run()
    while(True):
        print("Input something:")
        print(input())

if __name__ == "__main__":
    test()