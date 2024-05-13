from libs.web import json_client as c
from libs.gameui import *
import time

host = '10.129.247.130'  # Update server host when connecting to a network
port = 5555
client = c.JSONClient(host, port)
client.connect() 
while True:
    while not client.data:
        time.sleep(0.2)
    print(client.wait_data())
    inp = input(">")
    if inp == "x":
        break
    client.send_data(inp)


