import copy
from math import sqrt

class Game:

  def __init__(self, map_content=None):
    if(map_content == None):
      return
    self.map = [[j for j in i] for i in map_content.split("\n")][:-1]
    max_length = 0
    for i in self.map:
      if len(i) > max_length:
        max_length = len(i)

    for i in range(len(self.map)):
      j = len(self.map[i])
      while(j < max_length):
        self.map[i].append("-")
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
    self.path = []

  def can_move(self, direction):
    target = (self.player[0] + direction[0], self.player[1] + direction[1])
    if(self.map[target[0]][target[1]] == "#"):
      return False

    box_target = (target[0] + direction[0], target[1] + direction[1])
    if(target in self.boxes and (box_target in self.boxes or self.map[box_target[0]][box_target[1]] == "#")):
      return False

    return True

  def _move_player(self, direction):
    source = self.player
    target = (source[0] + direction[0], source[1] + direction[1])
    self.player = target

  def _move_box(self, source, direction):
    target = (source[0] + direction[0], source[1] + direction[1])
    self.boxes[self.boxes.index(source)] = target

  def _add_path(self, direction):
    self.path.append(
        "s" if (direction == (0, 1)) else
        "d" if (direction == (1, 0)) else
        "w" if (direction == (0, -1)) else
        "a"
    )

  def move(self, direction):
    self._add_path(direction)
    target = (self.player[0] + direction[0], self.player[1] + direction[1])
    if(target in self.boxes):
      self._move_box(target, direction)
    self._move_player(direction)

  def won(self):
    for box in self.boxes:
      if(box not in self.goals):
        return False
    return True

  def _trapped(self, box):
    lost_condition = [
        (0 + box[0], 1 + box[1]),
        (1 + box[0], 0 + box[1]),
        (0 + box[0], -1 + box[1]),
        (-1 + box[0], 0 + box[1]),
        (0 + box[0], 1 + box[1])
    ]

    for i in range(0, 4):
      if(self.map[lost_condition[i][0]][lost_condition[i][1]] == "#" and
         self.map[lost_condition[i + 1][0]][lost_condition[i + 1][1]] == "#"):
        return True
    return False

  def lost(self):
    for box in self.boxes:
      if(box not in self.goals and self._trapped(box)):
        return True
    return False

  def cost(self):
    def dist(p1, p2): return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    score = 0
    for box in self.boxes:
      for goal in self.goals:
        score += dist(box, goal)
      score += dist(box, self.player)
    return score

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
    result.boxes = copy.deepcopy(self.boxes)
    result.player = copy.deepcopy(self.player)
    result.goals = self.goals
    result.path = copy.deepcopy(self.path)
    return result

  def __eq__(self, other):
    return self.player == other.player and self.boxes == other.boxes

  def __ne__(self, other):
    return self != other

  def __hash__(self):
    # return hash("".join("".join(i) for i in self.map))
    # return hash(tuple([hash(tuple(l)) for l in self.map]))
    return hash(self.player) + hash(tuple(self.boxes))


if __name__ == "__main__":
  game = Game("""####
#-.#
#--###
#*@--#
#--$-#
#--###
####
""")
  print(game)
  while(True):
    first = True
    direction = (0, 0)
    while(first or not game.can_move(direction)):
      direction = input("")
      if direction == "w":
        direction = (0, -1)
      elif direction == "a":
        direction = (-1, 0)
      elif direction == "s":
        direction = (0, 1)
      elif direction == "d":
        direction = (1, 0)
      first = False
    game.move(direction)
    print(game)
    if(game.lost()):
      print("lost")
      break
    if(game.won()):
      print("won")
      break
