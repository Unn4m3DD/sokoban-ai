from copy import deepcopy


class Game:
  directions = [
      (-1, 0),
      (1, 0),
      (0, 1),
      (0, -1),
  ]
  directions_map = {
      (1, 0): "d",
      (-1, 0): "a",
      (0, 1): "s",
      (0, -1): "w",
  }

  def __init__(self, map_string=None):
    self.box_on_goal = 0
    if(map_string == None):
      return
    self.map = []
    self.boxes = []
    self.goals = []
    self.deadlocks = set()
    self.player = ()
    self.path = []
    horizontal_size = 0
    for y, line in enumerate(map_string.split("\n")[:-1]):
      self.map.append([])
      for x, item in enumerate(line):
        if(x > horizontal_size):
          horizontal_size = x
        if(item == "#"):
          self.map[y].append(item)
        else:
          self.map[y].append("-")
        if(item in ["$", "*"]):
          self.boxes.append((x, y))
        if(item in ["@", "+"]):
          self.player = (x, y)
        if(item in [".", "+", "*"]):
          self.goals.append((x, y))
    for line in self.map:
      for i in range(len(line), horizontal_size + 1):
        line.append("#")
    self.map = list(map(list, zip(*self.map)))
    self._calculate_simple_deadlocks()

  def _calculate_simple_deadlocks(self):
    reachable = set()
    for goal in self.goals:
      to_test = [goal]
      visited = set()
      while(len(to_test) != 0):
        current_test = to_test.pop(0)
        if(current_test in visited):
          continue
        visited.add(current_test)
        for direction in Game.directions:
          current_deadlock_test = (
              current_test[0] + direction[0], current_test[1] + direction[1])
          current_2offset = (
              current_test[0] + direction[0] * 2, current_test[1] + direction[1] * 2)
          if(self.map[current_deadlock_test[0]][current_deadlock_test[1]] == "#"):
            continue
          if(self.map[current_2offset[0]][current_2offset[1]] != "#"):
            to_test.append(current_deadlock_test)
            reachable.add(current_deadlock_test)
    for x in range(len(self.map)):
      for y in range(len(self.map[0])):
        if(self.map[x][y] != "#" and (x, y) not in self.goals and (x, y) not in reachable):
          self.deadlocks.add((x, y))

  def move(self, direction):
    self.path.append(Game.directions_map[direction])
    self.player = (self.player[0] + direction[0],
                   self.player[1] + direction[1])
    for i, box in enumerate(self.boxes):
      if(self.player == box):
        self.boxes[i] = (self.player[0] + direction[0],
                         self.player[1] + direction[1])

  def can_move(self, direction, source=(None)):
    if(source == None):
      source = self.player
    player_target = (source[0] + direction[0],
                     source[1] + direction[1])
    if(self.map[player_target[0]][player_target[1]] == "#"):
      return False
    box_target = (player_target[0] + direction[0],
                  player_target[1] + direction[1])
    virtual_boxes = [i for i in self.boxes if i != player_target]
    virtual_boxes.append(box_target)
    if(player_target in self.boxes and
       (self.map[box_target[0]][box_target[1]] == "#" or
            box_target in self.boxes or
            box_target in self.deadlocks or
            self._dynamic_deadlock(box_target, virtual_boxes))):
      return False
    return True

  def _dynamic_deadlock_adjacent(self, adjacent1, adjacent2,  box, virtual_boxes, virtual_wall=[]):
    return ((adjacent1 in virtual_wall or adjacent2 in virtual_wall
             or self.map[adjacent1[0]][adjacent1[1]] == "#" or self.map[adjacent2[0]][adjacent2[1]] == "#")
            or (adjacent1 in self.deadlocks and adjacent2 in self.deadlocks)
            or ((adjacent1 in virtual_boxes and
                 self._dynamic_deadlock(adjacent1, virtual_boxes, virtual_wall + [box])) or
                (adjacent2 in virtual_boxes and
                 self._dynamic_deadlock(adjacent2, virtual_boxes, virtual_wall + [box]))))

  def _dynamic_vertical_deadlock(self, box, virtual_boxes, virtual_wall=[]):
    adjacent1 = (box[0], box[1] + 1)
    adjacent2 = (box[0], box[1] - 1)
    return (self._dynamic_deadlock_adjacent(adjacent1, adjacent2, box, virtual_boxes, virtual_wall))

  def _dynamic_horizontal_deadlock(self, box, virtual_boxes, virtual_wall=[]):
    adjacent1 = (box[0] + 1, box[1])
    adjacent2 = (box[0] - 1, box[1])
    return (self._dynamic_deadlock_adjacent(adjacent1, adjacent2, box, virtual_boxes, virtual_wall))

  def _dynamic_deadlock(self, box, virtual_boxes, virtual_wall=[]):
    if(box in self.goals):
      return False
    if (self._dynamic_vertical_deadlock(box, virtual_boxes, virtual_wall) and
            self. _dynamic_horizontal_deadlock(box, virtual_boxes, virtual_wall)):
      return True

    return False

  def available_events(self):
    result = []
    to_test = [(self.player, [])]
    visited = set()
    while(len(to_test) != 0):
      current_test = to_test.pop(0)
      if(current_test[0] in visited):
        continue
      visited.add(current_test[0])
      for direction in Game.directions:
        current_target = (
            current_test[0][0] + direction[0], current_test[0][1] + direction[1])
        if(self.map[current_target[0]][current_target[1]] != "#"):
          if(current_target in self.boxes):
            if(self.can_move(direction, current_test[0])):
              result.append(current_test[1] + [direction])
          else:
            to_test.append((current_target, current_test[1] + [direction]))
    return result

  def perform_event(self, event):
    for direction in event:
      self.move(direction)

  def cost(self):
    # return len(self.path)
    def dist(a, b): return abs(a[0] - b[0]) + abs(a[1] - b[1])
    correct = 10
    cost = 0
    for box in self.boxes:
      if (box not in self.goals):
        min_cost = float("inf")
        for goal in self.goals:
          if(goal[1] == box[1]):
            cost -= 100
          distance = dist(box, goal)
          if(distance < min_cost):
            min_cost = distance
        cost += min_cost ** 2
      else:
        self.box_on_goal += 1
        correct <<= 2
    return cost - correct

  def won(self):
    for goal in self.goals:
      if(goal not in self.boxes):
        return False
    return True

  def __repr__(self): return str(self)

  def __str__(self):
    result = ""
    map_clone = deepcopy(self.map)
    for deadlock in self.deadlocks:
      map_clone[deadlock[0]][deadlock[1]] = "X"
    for goal in self.goals:
      map_clone[goal[0]][goal[1]] = "."
    for box in self.boxes:
      if(box in self.goals):
        map_clone[box[0]][box[1]] = "*"
      else:
        map_clone[box[0]][box[1]] = "$"
    if(self.player in self.goals):
      map_clone[self.player[0]][self.player[1]] = "+"
    else:
      map_clone[self.player[0]][self.player[1]] = "@"
    map_clone = list(map(list, zip(*map_clone)))
    for line in map_clone:
      result += "".join(line) + "\n"
    return result

  def better_than(self, other):
    if(self.box_on_goal > other.box_on_goal):
      return True
    if(self.box_on_goal < other.box_on_goal):
      return False
    return self.path < other.path

  def __ne__(self, other):
    return not (self == other)

  def __eq__(self, other):
    for box in self.boxes:
      if(box not in other.boxes):
        return False

    return self.player == other.player

  def __hash__(self):
    result = 0
    for i in self.boxes:
      result += i[0] + i[1]
    return result + hash(self.player)

  def clone(self):
    result = Game()
    result.map = self.map
    result.boxes = self.boxes[:]
    result.goals = self.goals[:]
    result.path = self.path[:]
    result.deadlocks = self.deadlocks
    result.player = self.player
    return result


if __name__ == "__main__":
  #   game = Game("""-#########
  # ##---#---##
  # #----#----#
  # #--$-#-$--#
  # #---*.*---#
  # ####.@.####
  # #---*.*---#
  # #--$-#-$--#
  # #----#----#
  # ##---#---##
  # -#########
  # """)
  game = Game(
      """
#####
#---###
#.-.--#
#---#-#
##-#--#
-#@$$-#
-#----#
-#--###
-####
""")
  # dirs = [(-1, 0), (-1, 0), (0, 1), (-1, 0),  (-1, 0)]
  # for d in dirs:
  #  if(game.can_move(d)):
  #    game.move(d)
  #  print(game)
  print(game)
  for i in (game.available_events()):
    print(i)
