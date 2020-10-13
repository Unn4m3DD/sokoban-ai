import asyncio
import getpass
import json
import os

import websockets
from mapa import Map
from agent import Agent
from time import sleep


async def agent_loop(server_address="localhost:8000", agent_name="student"):
  async with websockets.connect(f"ws://{server_address}/player", close_timeout=10000) as websocket:

    await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
    await websocket.recv()
    for i in range(26, 100):
      agent = Agent(open(f"levels/{i}.xsb").read())
      solution = agent.solve(1)
      while solution == None:
        try:
          await websocket.recv()
          solution = agent.solve(1)
        except websockets.exceptions.ConnectionClosedOK:
          print("Server has cleanly disconnected us")
          return
      if(solution == None):
        continue
      for key in solution:
        try:
          await websocket.recv()
          await websocket.send(
              json.dumps({"cmd": "key", "key": key})
          )
        except Exception as e:
          print(e)
        sleep(.2)


loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
