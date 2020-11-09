from game import Game
from collections import deque
import cProfile
pr = cProfile.Profile()


class State:
  def __init__(self, keys, game, cost):
    self.keys = keys
    self.game = game
    self.cost = cost

  def __hash__(self): return hash(self.game)
  def __eq__(self, other): 
    return other != None and self.game == other.game


def optimize(path, game):
  initial_game = game.clone()
  states = [State(None, initial_game, 0)]
  for i, move in enumerate(path):
    game.move(move)
    states.append(State([move], game.clone(), i + 1))

  states_hashset = set(states)
  for i in range(len(path) - 1, 0, -1):
  # for i in range(1, len(path)):
    
    if(states[i] == None): continue
    to_search = deque([states[i]])
    visited = set()
    while len(to_search) > 0 and to_search[0].cost < 15:
      current_state = to_search.popleft()
      if(current_state in visited):
        continue
      visited.add(states[i])
      if(current_state in states_hashset):
        idx = states.index(current_state)
        if(states[idx].cost > current_state.cost):
          states[idx] = current_state
          diff = current_state.cost - states[idx].cost
          for backward_idx in range(i + 1, idx):
            states_hashset.remove(states[backward_idx])
            states[backward_idx] = None
          for forward_idx in range(idx + 1, len(states)):
            states[forward_idx].cost -= diff

      for char, direction in (("s", (0, 1)), ("d", (1, 0)), ("w", (0, -1)), ("a", (-1, 0))):
        if(current_state.game.can_move(direction, simple=True)):
          game_clone = current_state.game.clone()
          game_clone.move(char)
          new_state = State(current_state.keys +
                            [char], game_clone, current_state.cost + 1)
          to_search.append(new_state)

  optimized_path = ""
  for state in states[1:]:
    if(state is not None):
      for key in state.keys:
        optimized_path += key
  return optimized_path

