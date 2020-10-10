import math
import json

from mapa import Map

class Agent:
  def __init__(self, map, timeout=math.inf):
    self.current = -1
    self.map = map
    self.plays = ["s", "a", "w", "d", "d", "d", "s", "a"]
    print(map.empty_goals)

  async def query_move(self, websocket):
    self.current += 1
    if(self.current < len(self.plays)):
      await websocket.send(
          json.dumps({"cmd": "key", "key": self.plays[self.current]})
      )