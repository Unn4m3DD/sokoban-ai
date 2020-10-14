import math
import json
from time import time
from game import Game

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class Agent:

  def __init__(self, original_map):
    self.current = -1
    self.original_game = Game(original_map)
    self.tested = set()
    self.to_solve = [(self.original_game, self.original_game.cost())]
    self.best_score = float("inf")

  def solve(self, timeout):
    initial_time = time()
    elapsed_time = 0
    while(len(self.to_solve) != 0 and elapsed_time < timeout):
      elapsed_time = (time()) - initial_time
      popped = self.to_solve.pop()
      if(popped[0] in self.tested):
        continue
      self.tested.add(popped[0])
      attempts = self._get_valid_attempts(popped[0])
      for attempt in attempts:
        if(attempt.won()):
          return attempt.path

        cost = attempt.cost()
        i = 0
        while(i < len(self.to_solve) and self.to_solve[i][1] > cost):
          i += 1

        self.to_solve.insert(i, (attempt, cost))

      new_best_score = self.to_solve[0][1]
      if(new_best_score < self.best_score):
        print(new_best_score)
        print(self.to_solve[0][0])
        self.best_score = new_best_score
    return None

  def _get_valid_attempts(self, game):
    global directions
    result = []
    for direction in directions:
      if(game.can_move(direction)):
        inner_game = game.clone()
        inner_game.move(direction)
        result.append(inner_game)
    return result
