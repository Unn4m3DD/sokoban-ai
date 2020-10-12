import math
import json

from student_game import Game

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class Agent:

  def __init__(self, original_map, timeout=math.inf):
    self.current = -1
    self.original_game = Game(original_map)
    self.tested = set()
    self.plays = self._solve()
    print(self.plays)

  def _solve(self):
    to_solve = [self.original_game]
    while(len(to_solve) != 0):
      poped = to_solve[0]
      to_solve = to_solve[1:]
      if(poped in self.tested):
        continue
      self.tested.add(poped)
      attempts = self._get_valid_attempts(poped)
      for attempt in attempts:
        if(attempt.won()):
          return attempt.path

        if(attempt.lost()):
          continue
        to_solve.append(attempt)

      #to_solve.sort(key=lambda x: x.score(), reverse=True)
    return []

  def _get_valid_attempts(self, game):
    global direction
    result = []
    for direction in directions:
      if(game.can_move(direction)):
        inner_game = game.clone()
        inner_game.move(direction)
        result.append(inner_game)
    return result

  def query_move(self):
    self.current += 1
    if(self.current < len(self.plays)):
      return self.plays[self.current]
    return None
