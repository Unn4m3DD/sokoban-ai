import math
import json

from student_game import Game

directions_map = {
    "s": (0, 1),
    "d": (1, 0),
    "w": (0, -1),
    "a": (-1, 0)
}


class Agent:

  def __init__(self, original_map, timeout=math.inf):
    self.current = -1
    self.original_game = Game(original_map)
    self.tested = set()
    self.plays = self._solve(self.original_game)[1]
    print(self.plays)

  def _solve(self, game):
    global directions_map
    if(game in self.tested):
      return False, []

    self.tested.add(game)
    valid_moves = []
    for direction in directions_map:
      if(game.can_move(directions_map[direction])):
        valid_moves.append((direction, directions_map[direction]))
    games = []

    for _ in range(len(valid_moves)):
      games.append(game.clone())

    for i in range(len(valid_moves)):
      # if(game.map[1][2] == "$" and game.map[2][4] == "$" and game.map[2][3] == "@" and valid_moves[i][0] == "a"):
      #  print("1\n",games[i])
      #  games[i].move(valid_moves[i][1])
      #  print("2\n", games[i])
      # else:
      games[i].move(valid_moves[i][1])

      if(games[i].won()):
        return True, [valid_moves[i][0]]
      # if(games[i].lost()):
      #  return False, []

      solution = self._solve(games[i])
      if(solution[0]):
        return True, [valid_moves[i][0]] + solution[1]

    return False, []

  def query_move(self):
    self.current += 1
    if(self.current < len(self.plays)):
      return self.plays[self.current]
    return None
