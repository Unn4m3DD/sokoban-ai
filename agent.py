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
    if(game in self.tested):
      return False, []
    self.tested.add(game)

    attempts = self._get_valid_attempts(game)

    for attempt in attempts:
      attempt[2].move(attempt[1])

      if(attempt[2].won()):
        return True, [attempt[0]]

      if(attempt[2].lost()):
        continue

    attempts = sorted(attempts, key=lambda x: x[2].score())
    for attempt in attempts:
      solution = self._solve(attempt[2])
      if(solution[0]):
        return True, [attempt[0]] + solution[1]

    return False, []

  def _get_valid_attempts(self, game):
    global directions_map
    result = []
    for direction in directions_map:
      if(game.can_move(directions_map[direction])):
        result.append(
            (direction, directions_map[direction], game.clone())
        )
    return result

  def query_move(self):
    self.current += 1
    if(self.current < len(self.plays)):
      return self.plays[self.current]
    return None
