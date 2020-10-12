import copy

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
    self.path = []

  def can_move(self, direction):
    target = (self.player[0] + direction[0], self.player[1] + direction[1])
    if(self.map[target[0]][target[1]] == "#"):
      return False

    if(self.map[target[0]][target[1]] in ["$", "*"] and
       self.map[target[0] + direction[0]][target[1] + direction[1]] in ["$", "*", "#"]):
      return False

    return True

  def _move_player(self, direction):
    source = self.player
    target = (source[0] + direction[0], source[1] + direction[1])
    target_contains_diamond = self.map[target[0]][target[1]] == "."
    self.map[target[0]][target[1]] = "@" if not target_contains_diamond else "+"
    source_contains_diamond = self.map[source[0]][source[1]] == "+"
    self.map[source[0]][source[1]] = "-" if not source_contains_diamond else "."
    self.player = target

  def _move_box(self, source, direction):
    target = (source[0] + direction[0], source[1] + direction[1])
    source_contains_diamond = self.map[source[0]][source[1]] == "*"
    self.map[source[0]][source[1]] = "-" if not source_contains_diamond else "."
    target_contains_diamond = self.map[target[0]][target[1]] == "."
    self.map[target[0]][target[1]] = "$" if not target_contains_diamond else "*"
    for i in range(len(self.boxes)):
      if(self.boxes[i] == source):
        self.boxes[i] = target

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
    if(self.map[target[0]][target[1]] in ["$", "*"]):
      self._move_box(target, direction)
    self._move_player(direction)

  def won(self):
    for box in self.boxes:
      if(self.map[box[0]][box[1]] == "$"):
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
      if(self.map[box[0]][box[1]] == "$" and self._trapped(box)):
        return True
    return False

  def score(self):
    def dist(p1, p2): return (p1[0] * p2[0])**2 + (p1[1] * p2[1])**2
    score = 0
    for box in self.boxes:
      for goal in self.goals:
        score += dist(box, goal)
    return score

  def __str__(self):
    local_map = list(map(list, zip(*self.map)))
    res = ""
    for row in local_map:
      for item in row:
        res += str(item)
      res += '\n'
    return res

  def clone(self):
    result = Game()
    result.map = copy.deepcopy(self.map)
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
    return hash("".join("".join(i) for i in self.map))
    # return hash(tuple([hash(tuple(l)) for l in self.map]))
    # return hash(self.player) + hash(tuple(self.boxes))


if __name__ == "__main__":
  game = Game("""####--
#-.#--
#$-###
#.@--#
#-$--#
#--###
####--
""")

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
      else:
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
