import math
import json

from mapa import Map

class Agent:
  def __init__(self, map, timeout=math.inf):
    self.current = -1
    self.map = map
    self.plays = ["s", "a", "w", "d", "d", "d", "s", "a"]

  async def query_move(self, websocket):
    self.current += 1
    if(self.current < len(self.plays)):
      await websocket.send(
          json.dumps({"cmd": "key", "key": self.plays[self.current]})
    )
    print(self.map)
    dir = (0,0)
    if self.plays[self.current] == "w":
      dir = (0,1)
    elif self.plays[self.current] == "a":
      dir = (-1,0)
    elif self.plays[self.current] == "s":
      dir = (0,-1)
    else:
      dir = (1,0)
    self.map.move(dir)

