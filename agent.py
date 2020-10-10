import math
import json

from student_game import Game

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
dir_map = {
  (0, 1) : "s",
  (1, 0) : "d",
  (0, -1) : "w", 
  (-1, 0) : "a"
}

class Agent:

  def __init__(self, original_map, timeout=math.inf):
    self.current = -1
    self.original_game = Game(original_map)
    self.tested = []
    self.plays = self._solve(self.original_game)[1]
    print(self.plays)

  def _solve(self, game):
    if(game.map[1][2] == "$" and game.map[2][4] == "$"):
      print(game)
      print()
    hash_code = str(game)
    if(hash_code in self.tested):
      return False, []
    self.tested.append(hash_code)
    global directions
    available_directions = []
    for direction in directions:
      if(game.can_move(direction)):
        available_directions.append(direction)
    games = [game.clone() for i in range(len(available_directions))]
    for i in range(len(games)):
      games[i].move(available_directions[i])
      if(games[i].won()):
        return True, [dir_map[available_directions[i]]]
      if(games[i].lost()):
        return False, []
      solution = self._solve(games[i])
      if(solution[0]):
        return True, [dir_map[available_directions[i]]] + solution[1]
    return False, []

  async def query_move(self, websocket):
    self.current += 1
    if(self.current < len(self.plays)):
      await websocket.send(
          json.dumps({"cmd": "key", "key": self.plays[self.current]})
      )
