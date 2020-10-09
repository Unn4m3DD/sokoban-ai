import asyncio
import getpass
import json
import os

import websockets
from mapa import Map


async def agent_loop(server_address="localhost:8000", agent_name="student"):
  async with websockets.connect(f"ws://{server_address}/player") as websocket:

    await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
    msg = await websocket.recv()
    game_properties = json.loads(msg)

    mapa = Map(game_properties["map"])
    print(mapa)

    while True:
      try:
        state = json.loads(
            await websocket.recv()
        )
        input("")
        game_properties = json.loads(msg)

        mapa = Map(game_properties["map"])
        print(Map(f"levels/{state['level']}.xsb"))
        print(mapa)
        print(state)
        await websocket.send(
            json.dumps({"cmd": "key", "key": "w"})
        )
      except websockets.exceptions.ConnectionClosedOK:
        print("Server has cleanly disconnected us")
        return


loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
