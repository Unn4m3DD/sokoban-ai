from time import time
from game import Game
from collections import deque

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class Agent:
  curral_strategy_threshold = 100

  def __init__(self, original_map):
    self.original_game = Game(original_map)
    self.tested = set()
    self.to_solve = deque()
    self.to_solve.append((self.original_game,  self.original_game.cost()))
    self.best_cost = float("inf")
    self.elapsed_time = 0

  def solve(self, timeout):
    initial_time = time()
    elapsed_time = 0
    while(elapsed_time < timeout and self.to_solve != []):
      elapsed_time = time() - initial_time
      if(self.elapsed_time + elapsed_time > Agent.curral_strategy_threshold):
        Agent.curral_strategy_threshold = float("inf")
        Game.curral_and_greedy = True
        self.to_solve = [(self.original_game, self.original_game.cost())]
        self.tested = set()
      popped = self.to_solve.pop()
      if(popped[0] in self.tested):
        continue
      self.tested.add(popped[0])

      attempts = self._get_valid_attempts(popped[0])
      for attempt in attempts:
        if(attempt.won()):
          Game.curral_and_greedy = False
          return attempt.path

        cost = attempt.cost()
        i = 0
        to_solve_size = len(self.to_solve)
        while(i < to_solve_size and self.to_solve[i][1] > cost):
          i += 1

        self.to_solve.insert(i, (attempt, cost))
        # print(self.to_solve[-1][0])
        # print(self.to_solve[-1][1])
        if(self.best_cost >= self.to_solve[-1][1]):
          self.best_cost = self.to_solve[-1][1]

          # print(self.to_solve[-1][1])
          # print()
    self.elapsed_time += elapsed_time
    return None

  def _get_valid_attempts(self, game):
    result = []
    for (event, is_curral) in game.available_events():
      inner_game = game.clone()
      inner_game.perform_event(event)
      if(is_curral):
        inner_game.curral_count += 1
      result.append(inner_game)
    return result
