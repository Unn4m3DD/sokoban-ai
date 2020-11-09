import copy
from math import sqrt
import time
from collections import deque
directions = {"s": (0, 1),
              "d": (1, 0),
              "w": (0, -1),
              "a": (-1, 0)}



class Game:
  curral_and_greedy = False

  def __init__(self, map_content=None):
    if(map_content == None):
      return
    self.map = [[j for j in i] for i in map_content.split("\n")][:-1]
    self.curral_count = 0
    max_length = 0
    for i in self.map:
      if len(i) > max_length:
        max_length = len(i)
    for i in range(len(self.map)):
      j = len(self.map[i])
      while(j < max_length):
        self.map[i].append("#")
        j += 1

    self.map = list(map(list, zip(*self.map)))
    self.boxes = []
    self.goals = []
    self.player = ()
    for x in range(len(self.map)):
      for y in range(len(self.map[x])):
        if(self.map[x][y] in ["@", "+"]):
          self.player = (x, y)
        if(self.map[x][y] in ["$", "*"]):
          self.boxes.append((x, y))
        if(self.map[x][y] in ["+", "*", "."]):
          self.goals.append((x, y))
    for x in range(len(self.map)):
      for y in range(len(self.map[x])):
        if self.map[x][y] in [".", "$", "*", "@", "+"]:
          self.map[x][y] = "-"
    self._bfs_available_positions()
    self.deadlocks = self._static_deadlocks()
    for goal in self.goals:
      if(goal in self.deadlocks):
        self.deadlocks.remove(goal)
    self.path = []

    matched = [-1 for i in self.boxes]  # index box, content goal
    distances = []  # (box, goal, distance)
    for box in range(len(self.boxes)):
      for goal in range(len(self.goals)):
        distances.append((box, goal, self.push_distance(
            self.boxes[box], self.goals[goal])))
    distances = sorted(distances, key=lambda e: e[2])

    for pair in distances:
      if(matched[pair[0]] == -1 and pair[1] not in matched):
        matched[pair[0]] = pair[1]

    self.boxes = [self.boxes[i] for i in matched]

  def _static_deadlocks(self):
    deadlocks = set()
    for x in range(1, len(self.map) - 1):
      for y in range(1, len(self.map[x]) - 1):
        if(self.map[x][y] == "#"):
          continue
        position = (x, y)
        if(position not in self.goals and self._trapped(position)):
          deadlocks.add(position)
          continue
        if(self._cant_go_diamond_direction(position)):
          deadlocks.add(position)
          continue
    return deadlocks

  def _bfs_available_positions(self):
    visited = set()
    queue = deque()
    queue.append(self.player)
    while(len(queue) != 0):
      item = queue.popleft()
      if(item in visited):
        continue
      visited.add(item)
      for i in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        pos = (item[0] + i[0], item[1] + i[1])
        if(self.map[pos[0]][pos[1]] != "#"):
          queue.append(pos)
    for i in range(len(self.map)):
      for j in range(len(self.map[i])):
        self.map[i][j] = "#"

    for pos in visited:
      self.map[pos[0]][pos[1]] = "-"

  def _dynamic_deadlock_adjacent(self, adjacent1, adjacent2,  box, virtual_boxes, virtual_wall=[], ignore_goals=False):
    return ((adjacent1 in virtual_wall or adjacent2 in virtual_wall
             or self.map[adjacent1[0]][adjacent1[1]] == "#" or self.map[adjacent2[0]][adjacent2[1]] == "#")
            or (adjacent1 in self.deadlocks and adjacent2 in self.deadlocks)
            or ((adjacent1 in virtual_boxes and
                 self._dynamic_deadlock(adjacent1, virtual_boxes, virtual_wall + [box], ignore_goals)) or
                (adjacent2 in virtual_boxes and
                 self._dynamic_deadlock(adjacent2, virtual_boxes, virtual_wall + [box], ignore_goals))))

  def _dynamic_vertical_deadlock(self, box, virtual_boxes, virtual_wall=[], ignore_goals=False):
    adjacent1 = (box[0], box[1] + 1)
    adjacent2 = (box[0], box[1] - 1)
    return (self._dynamic_deadlock_adjacent(adjacent1, adjacent2, box, virtual_boxes, virtual_wall, ignore_goals))

  def _dynamic_horizontal_deadlock(self, box, virtual_boxes, virtual_wall=[], ignore_goals=False):
    adjacent1 = (box[0] + 1, box[1])
    adjacent2 = (box[0] - 1, box[1])
    return (self._dynamic_deadlock_adjacent(adjacent1, adjacent2, box, virtual_boxes, virtual_wall, ignore_goals))

  def _dynamic_deadlock(self, box, virtual_boxes, virtual_wall=[], ignore_goals=False):
    if(not ignore_goals and box in self.goals):
      return False
    if (self._dynamic_vertical_deadlock(box, virtual_boxes, virtual_wall, ignore_goals) and
            self. _dynamic_horizontal_deadlock(box, virtual_boxes, virtual_wall, ignore_goals)):
      return True

    return False

  def _curral_locked(self, box, virtual_boxes):
    visited = set()
    queue = deque()
    queue.append(box)
    while(len(queue) != 0):
      item = queue.popleft()
      if(item in visited):
        continue
      visited.add(item)
      for i in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        pos = (item[0] + i[0], item[1] + i[1])
        if(pos == self.player):
          return False
        if(self.map[pos[0]][pos[1]] != "#"):
          if (pos not in virtual_boxes or not self._dynamic_deadlock(pos, virtual_boxes, [], True)):
            queue.append(pos)
    return True

  def can_move(self, direction, source=None, simple=False):
    if(source == None):
      source = self.player
    target = (source[0] + direction[0], source[1] + direction[1])
    if(self.map[target[0]][target[1]] == "#"):
      return False

    box_target = (target[0] + direction[0], target[1] + direction[1])
    virtual_boxes = [i for i in self.boxes if i != target]
    virtual_boxes.append(box_target)
    if(target in self.boxes):
      if (
          box_target in self.boxes or
          self.map[box_target[0]][box_target[1]] == "#" or
          box_target in self.deadlocks or
          not simple and self._dynamic_deadlock(box_target, virtual_boxes)
      ):
        return False
    if(not simple and Game.curral_and_greedy):
      for box in virtual_boxes:
        if(box not in self.goals):
          if(self._curral_locked(box, virtual_boxes)):
            return False
    return True

  def _move_player(self, direction):
    source = self.player
    target = (source[0] + direction[0], source[1] + direction[1])
    self.player = target

  def _move_box(self, source, direction):
    target = (source[0] + direction[0], source[1] + direction[1])
    self.boxes[self.boxes.index(source)] = target

  def move(self, direction_char):
    global directions
    self.path.append(direction_char)
    direction = directions[direction_char]
    target = (self.player[0] + direction[0], self.player[1] + direction[1])
    if(target in self.boxes):
      self._move_box(target, direction)
    self._move_player(direction)

  def available_events(self):
    def is_curral(direction, start):
      if(not Game.curral_and_greedy):
        return False
      result = []
      visited = set()
      queue = deque()
      start = (start[0] + direction[0] + direction[0],
               start[1] + direction[1] + direction[1])
      queue.append(start)
      while(len(queue) != 0):
        item = queue.popleft()
        if(item in visited):
          continue
        if(item == self.player):
          return False
        visited.add(item)
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
          pos = (item[0] + direction[0], item[1] + direction[1])
          if(self.map[pos[0]][pos[1]] != "#" and pos not in self.boxes):
            queue.append(pos)
      return True
    result = []
    visited = set()
    queue = deque()
    queue.append((self.player, []))
    while(len(queue) != 0):
      item = queue.popleft()
      if(item[0] in visited):
        continue
      visited.add(item[0])
      for char, direction in (("s", (0, 1)), ("d", (1, 0)), ("w", (0, -1)), ("a", (-1, 0))):
        pos = (item[0][0] + direction[0], item[0][1] + direction[1])
        if(self.map[pos[0]][pos[1]] != "#" and pos not in self.boxes):
          queue.append((pos, item[1] + [char]))
        elif(pos in self.boxes and self.can_move(direction, item[0])):
          result.append((item[1] + [char], is_curral(direction, item[0])))
    return result

  def perform_event(self, event):
    global directions
    for action in event:
      self.move(action)
    last_action = event[-1]
    direction = directions[last_action]

    while False:
      destinaton = (self.player[0] + direction[0],
                    self.player[1] + direction[1])
      if(destinaton in self.goals):
        print("end\n", self)
        return
      if(last_action in ["a", "d"]):
        bound1 = (destinaton[0] - direction[0], destinaton[1] + 1)
        bound2 = (destinaton[0] - direction[0], destinaton[1] - 1)
      else:
        bound1 = (destinaton[0] + 1, destinaton[1] - direction[1])
        bound2 = (destinaton[0] - 1, destinaton[1] - direction[1])
      if(self.map[bound1[0]][bound1[1]] == "#"
         and self.map[bound2[0]][bound2[1]] == "#"
         and self.can_move(direction)):
        self.move(last_action)
      else:
        print("end\n", self)
        return

  def won(self):
    for box in self.boxes:
      if(box not in self.goals):
        return False
    return True

  def _trapped(self, box, virtual_walls=[]):
    lost_condition = [
        (0 + box[0], 1 + box[1]),
        (1 + box[0], 0 + box[1]),
        (0 + box[0], -1 + box[1]),
        (-1 + box[0], 0 + box[1]),
        (0 + box[0], 1 + box[1])
    ]

    for i in range(0, 4):
      if((self.map[lost_condition[i][0]][lost_condition[i][1]] == "#" or lost_condition[i] in virtual_walls) and
         (self.map[lost_condition[i + 1][0]][lost_condition[i + 1][1]] == "#" or lost_condition[i + 1] in virtual_walls)):
        return True
    return False

  def _cant_go_diamond_direction_horizontal(self, box):
    horizontal_match = False
    for goal in self.goals:
      if(goal[1] == box[1]):
        horizontal_match = True

    if(not horizontal_match):
      horizontally_trapped = True
      for x in range(len(self.map)):
        for y in range(box[1]):
          if(self.map[x][y] != "#"):
            horizontally_trapped = False
            break
      if(horizontally_trapped):
        return True

      horizontally_trapped = True
      for x in range(len(self.map)):
        for y in range(box[1] + 1, len(self.map[box[0]])):
          if(self.map[x][y] != "#"):
            horizontally_trapped = False
            break
      if(horizontally_trapped):
        return True
    return False

  def _cant_go_diamond_direction_vertical(self, box):
    vertical_match = False
    for goal in self.goals:
      if(goal[0] == box[0]):
        vertical_match = True

    if(not vertical_match):
      vertically_trapped = True
      for x in range(box[0]):
        for y in range(len(self.map[box[0]])):
          if(self.map[x][y] != "#"):
            vertically_trapped = False
            break
      if(vertically_trapped):
        return True

      vertically_trapped = True
      for x in range(box[0] + 1, len(self.map)):
        for y in range(len(self.map[box[0]])):
          if(self.map[x][y] != "#"):
            vertically_trapped = False
            break
      if(vertically_trapped):
        return True
    return False

  def _cant_go_diamond_direction(self, box):
    if(self._cant_go_diamond_direction_horizontal(box)):
      return True
    if(self._cant_go_diamond_direction_vertical(box)):
      return True
    return False

  def manhattan(self, p1, p2): return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

  def euclidian(self, p1, p2):
    return (p1[0] - p2[0])**2 + abs(p1[1] - p2[1])**2

  def push_distance(self, p1, p2):
    # code below not used cause it's slow af
    to_test = [(p1, 0, self.manhattan(p1, p2))]
    visited = set()
    while(to_test != []):
      popped = to_test.pop()
      if(popped[0] in visited):
        continue
      visited.add(popped[0])
      if(popped[0] == p2):
        return popped[1]
      for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_point = (popped[0][0] + direction[0],
                     popped[0][1] + direction[1])
        if(self.map[new_point[0]][new_point[1]] == "#"):
          continue
        item = (new_point, popped[1] + 1, self.manhattan(new_point, p2))
        i = 0
        while(i < len(to_test) and to_test[i][2] > item[2]):
          i += 1
        to_test.insert(i, item)

  def cost(self):
    # return len(self.path)
    cost = 0
    if(Game.curral_and_greedy):
      for box, goal in zip(self.boxes, self.goals):
        cost += self.manhattan(box, goal)
      return cost - self.curral_count * 1

    correct = 10
    for box in self.boxes:
      if (box not in self.goals):
        min_cost = float("inf")
        for goal in self.goals:
          distance = self.manhattan(box, goal)
          if(distance < min_cost):
            min_cost = self.manhattan(box, goal)
        cost += min_cost ** 2
      else:
        correct <<= 2
    return cost - correct

  def __str__(self):
    local_map = list(self.map)
    for box in self.boxes:
      if(box in self.goals):
        tmp = list(local_map[box[0]])
        tmp[box[1]] = "*"
        local_map[box[0]] = "".join(tmp)
      else:
        tmp = list(local_map[box[0]])
        tmp[box[1]] = "$"
        local_map[box[0]] = "".join(tmp)

    for goal in self.goals:
      if(goal not in self.boxes and goal != self.player):
        tmp = list(local_map[goal[0]])
        tmp[goal[1]] = "."
        local_map[goal[0]] = "".join(tmp)

    for deadlock in self.deadlocks:
      if(deadlock not in self.boxes and deadlock != self.player):
        tmp = list(local_map[deadlock[0]])
        tmp[deadlock[1]] = "X"
        local_map[deadlock[0]] = "".join(tmp)

    tmp = list(local_map[self.player[0]])
    tmp[self.player[1]] = "@" if self.player not in self.goals else "+"
    local_map[self.player[0]] = "".join(tmp)
    local_map = list(map(list, zip(*local_map)))
    res = ""
    for row in local_map:
      for item in row:
        res += str(item)
      res += '\n'
    return res

  def clone(self):
    result = Game()
    result.map = self.map
    result.boxes = self.boxes[:]
    result.player = tuple(self.player)
    result.goals = self.goals
    result.curral_count = self.curral_count
    result.deadlocks = self.deadlocks
    result.path = self.path[:]
    return result

  def __eq__(self, other):
    return self.player == other.player and self.boxes == other.boxes

  def __ne__(self, other):
    return self != other

  def __hash__(self):
    # return hash(str(self))
    # return hash(tuple([hash(tuple(l)) for l in self.map]))
    result = 0
    for i in self.boxes:
      result += i[0] + i[1]
    return result +  hash(self.player)


if __name__ == "__main__":
  game = Game("""-#########
##---#---##
#----#----#
#--$-#-$--#
#---*.*---#
####.@.####
#---*.----#
#--$-#-$--#
#----#----#
##---#---##
-#########
""")
  print(game.available_events())
  print(game)
  while(True):
    first = True
    direction = input("")
    while(not game.can_move(directions[direction])):
      direction = input("")
    game.move(direction)
    print(game)
    if(game.won()):
      print("won")
      break
