import math
import json
from time import time_ns
from student_game import Game

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class Agent:

  def __init__(self, original_map, timeout=math.inf):
    self.current = -1
    self.original_game = Game(original_map)
    self.tested = set()
    self.to_solve = [self.original_game]

  def solve(self, timeout):
    initial_time = time_ns() / 10e9
    elapsed_time = 0
    while(len(self.to_solve) != 0 and elapsed_time < timeout):
      popped = self.to_solve[0]
      self.to_solve = self.to_solve[1:]
      if(popped in self.tested):
        continue
      self.tested.add(popped)
      attempts = self._get_valid_attempts(popped)
      for attempt in attempts:
        if(attempt.won()):
          return attempt.path

        if(attempt.lost()):
          continue
        self.to_solve.append(attempt)

      self.to_solve.sort(key=lambda x: x.score(), reverse=False)
      elapsed_time = initial_time - time_ns() / 10e9
    return []

  def _get_valid_attempts(self, game):
    global directions
    result = []
    for direction in directions:
      if(game.can_move(direction)):
        inner_game = game.clone()
        inner_game.move(direction)
        result.append(inner_game)
    return result

