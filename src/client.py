import asyncio
import getpass
import json
import os
from time import time
import websockets
from agent import Agent
from time import sleep


async def agent_loop(server_address="localhost:8000", agent_name="student"):
  async with websockets.connect(f"ws://{server_address}/player", close_timeout=10000) as websocket:

    await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
    server_request = json.loads(await websocket.recv())
    print(server_request)
    fps = int(server_request["fps"])
    level = server_request["map"]
    agent = Agent(open(level).read())
    while True:
      level = json.loads(await websocket.recv())["level"]
      agent = Agent(open(f"levels/{level}.xsb").read())
      solution = None
      try:
        while solution == None:
          start_time = time()
          solution = agent.solve(100)
          elapsed_time = time() - start_time

          for i in range(0, int(elapsed_time * fps + 10)):
            await websocket.recv()

        for key in solution:
          await websocket.send(
              json.dumps({"cmd": "key", "key": key})
          )
          await websocket.recv()

      except websockets.exceptions.ConnectionClosedOK:
        print("Server has cleanly disconnected us")
        return


def main():
  loop = asyncio.get_event_loop()
  SERVER = os.environ.get("SERVER", "localhost")
  PORT = os.environ.get("PORT", "8000")
  NAME = "93357"
  loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))


if __name__ == "__main__":
  main()
