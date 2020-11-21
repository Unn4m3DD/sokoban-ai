import asyncio
from time import time
from src.new_game import Game
from collections import deque
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class Agent:

  def __init__(self, original_map):
    self.original_game = Game(original_map)
    self.visited = set()
    self.to_solve = deque()
    self.to_solve.append((self.original_game, self.original_game.cost()))
    self.best_cost = float("inf")
    self.best_game = Game(original_map)

  async def solve(self, global_timeout=300, fps=10):
    initial_time = time()
    elapsed_time = 0
    while(self.to_solve != []):
      elapsed_time = time() - initial_time
      if(elapsed_time > global_timeout - len(self.best_game.path) / (fps - 4)):
        return self.best_game.path
      # print(self.visited)
      popped = self.to_solve.pop()

      attempts = self._get_valid_attempts(popped[0])
      #print(popped[0])
      for attempt in attempts:
        if(attempt.won()):
          return attempt.path
        if(attempt in self.visited):
          continue

        cost = attempt.cost()
        # must be called after cost
        if attempt.better_than(self.best_game):
          # print(attempt)
          self.best_game = attempt
        i = 0
        to_solve_size = len(self.to_solve)
        while(i < to_solve_size and self.to_solve[i][1] > cost):
          i += 1

        self.to_solve.insert(i, (attempt, cost))
        self.visited.add(attempt)
        # print(self.to_solve[-1][0])
        # print(self.to_solve[-1][1])
        if(self.best_cost >= self.to_solve[-1][1]):
          self.best_cost = self.to_solve[-1][1]

          # print(self.to_solve[-1][1])
          # print()
      await asyncio.sleep(0)
    return None

  def _get_valid_attempts(self, game):
    result = []
    for event in game.available_events():
      inner_game = game.clone()
      inner_game.perform_event(event)
      result.append(inner_game)
    return result
