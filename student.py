import asyncio
import getpass
import json
import os

import websockets
from mapa import Map
from agent import Agent

async def agent_loop(server_address="localhost:8000", agent_name="student"):
  async with websockets.connect(f"ws://{server_address}/player") as websocket:

    await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
    msg = await websocket.recv()
    game_properties = json.loads(msg)

    agent = Agent(
        Map(game_properties["map"])
    )
    while True:
      try:
        state = json.loads(
            await websocket.recv()
        )
        await agent.query_move(websocket)
        #print(state)
      except websockets.exceptions.ConnectionClosedOK:
        print("Server has cleanly disconnected us")
        return


loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
