import asyncio
import getpass
import json
import os

import websockets
from mapa import Map
from agent import Agent
from time import sleep


async def agent_loop(server_address="localhost:8000", agent_name="student"):
  async with websockets.connect(f"ws://{server_address}/player") as websocket:

    await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
    await websocket.recv()
    for i in range(1, 100):
      agent = Agent(open(f"levels/{i}.xsb").read())
      queried = agent.query_move()
      while queried != None:
        try:
          print(await websocket.recv())
          await websocket.send(
              json.dumps({"cmd": "key", "key": queried})
          )
          queried = agent.query_move()
          sleep(.2)
        except websockets.exceptions.ConnectionClosedOK:
          print("Server has cleanly disconnected us")
          return


loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
