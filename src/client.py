import asyncio
import getpass
import json
import os
from time import time
import websockets
from src.agent import Agent
from time import sleep
import threading


def set_interval(func, sec):
  def func_wrapper():
    set_interval(func, sec)
    func()
  t = threading.Timer(sec, func_wrapper)
  t.start()
  return t


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
      outer_start_time = time()
      try:
        thread = set_interval(websocket.recv, 1 / (fps + 1))
        while solution == None:
          start_time = time()
          solution = agent.solve(1, 300, fps)
          elapsed_time = time() - start_time
        thread.cancel()
        for key in solution:
          await websocket.send(
              json.dumps({"cmd": "key", "key": key})
          )
          await websocket.recv()
        print(
            f"solved {level} in {round((time() - outer_start_time) * 100) / 100} seconds")
      except websockets.exceptions.ConnectionClosedOK:
        print("Server has cleanly disconnected us")
        return


def main():
  loop = asyncio.get_event_loop()
  SERVER = os.environ.get("SERVER", "localhost")
  PORT = os.environ.get("PORT", "8000")
  NAME = "andre"
  loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))


if __name__ == "__main__":
  main()
