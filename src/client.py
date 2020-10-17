import asyncio
import getpass
import json
import os

import websockets
from agent import Agent
from time import sleep


async def agent_loop(server_address="localhost:8000", agent_name="student"):
  async with websockets.connect(f"ws://{server_address}/player", close_timeout=10000) as websocket:

    await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
    await websocket.recv()
    for i in range(1, 156):
      agent = Agent(open(f"levels/{i}.xsb").read())
      solution = None
      while solution == None:
        try:
          await websocket.recv()
          solution = agent.solve(.1)
        except websockets.exceptions.ConnectionClosedOK:
          print("Server has cleanly disconnected us")
          return
      if(solution == None):
        continue
      await websocket.recv()
      await websocket.send(
          json.dumps({"cmd": "keys", "keys": "".join(solution)})
      )


def main():
  loop = asyncio.get_event_loop()
  SERVER = os.environ.get("SERVER", "localhost")
  PORT = os.environ.get("PORT", "8000")
  NAME = "93357"
  loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))


if __name__ == "__main__":
  main()
