import math
import json


class Agent:
  def __init__(self, map, timeout=math.inf):
    self.current = -1
    self.plays = ["s", "a", "w", "d", "d", "d", "s", "a"]

  async def query_move(self, websocket):
    self.current += 1
    if(self.current < len(self.plays)):
      await websocket.send(
          json.dumps({"cmd": "key", "key": self.plays[self.current]})
      )
