import math
import json

from student_game import Game

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
class Agent:

  def __init__(self, original_map, timeout=math.inf):
    self.current = -1
    self.original_game = Game(original_map)
    self.plays = self._solve(self.original_game)

  def _solve(self, game):
    available_directions = []
    for direction in directions:
      if(game.can_move(direction)):
        available_directions.append(direction)
    return []

  async def query_move(self, websocket):
    self.current += 1
    if(self.current < len(self.plays)):
      await websocket.send(
          json.dumps({"cmd": "key", "key": self.plays[self.current]})
      )
