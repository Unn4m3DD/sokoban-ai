from time import time
from game import Game

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class Agent:

  def __init__(self, original_map):
    original_game = Game(original_map)
    self.tested = set()
    self.to_solve = [(original_game, original_game.cost())]
    self.best_cost = float("inf")

  def solve(self, timeout):
    initial_time = time()
    elapsed_time = 0
    while(elapsed_time < timeout and self.to_solve != []):
      elapsed_time = time() - initial_time

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
        to_solve_size = len(self.to_solve)
        while(i < to_solve_size and self.to_solve[i][1] > cost):
          i += 1

        self.to_solve.insert(i, (attempt, cost))
        if(self.best_cost > self.to_solve[-1][1]):
          self.best_cost = self.to_solve[-1][1]
          #print(self.to_solve[-1][0])
          #print(self.to_solve[-1][1])
          #print()
    return None

  def _get_valid_attempts(self, game):
    result = []
    for event in game.available_events():
      inner_game = game.clone()
      inner_game.perform_event(event)
      result.append(inner_game)
    return result
