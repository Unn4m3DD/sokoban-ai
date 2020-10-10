import consts


class Game:

  def __init__(self, map_content):
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
    for x in range(len(self.map)):
      for y in range(len(self.map[x])):
        if(self.map[x][y] in ["@", "+"]):
          self.player = (x, y)
        if(self.map[x][y] in ["$", "*"]):
          self.boxes.append((x, y))

  def can_move(self, direction):
    target = (self.player[0] + direction[0], self.player[1]+direction[1])
    if(self.map[target[0]][target[1]] == "#"):
      return False

    if(self.map[target[0]][target[1]] in ["$", "*"] and self.map[target[0]][target[1]] not in ["$", "*", "#"]):
      return False
    return True

  def _move_player(self, direction):
    source = self.player
    target = (source[0] + direction[0], source[1] + direction[1])
    target_contains_diamond = self.map[target[0]][target[1]] == "."
    self.map[target[0]][target[1]] = "@" if not target_contains_diamond else "+"
    source_contains_diamond = self.map[source[0]][source[1]] == "+"
    self.map[source[0]][source[1]] = "-" if not source_contains_diamond else "."

  def _move_box(self, source, direction):
    target = (source[0] + direction[0], source[1] + direction[1])
    source_contains_diamond = self.map[source[0]][source[1]] == "*"
    self.map[source[0]][source[1]] = "-" if not source_contains_diamond else "."
    target_contains_diamond = self.map[target[0]][target[1]] == "."
    self.map[target[0]][target[1]] = "$" if not target_contains_diamond else "*"
    for i in range(len(self.boxes)):
      if(self.boxes[i] == source):
        self.boxes[i] = target

  def move(self, direction):
    target = (self.player[0] + direction[0], self.player[1]+direction[1])
    if(self.map[target[0]][target[1]] in ["$", "*"]):
      self._move_box(target, direction)
    self._move_player(direction)
    self.player = target

  def won(self):
    for box in self.boxes:
      if(self.map[box[0]][box[1]] == "$"):
        return False
    return True

  def _trapped(self, box):
    lost_cond = [
        (0 + box[0], 1 + box[1]),
        (1 + box[0], 0 + box[1]),
        (0 + box[0], -1 + box[1]),
        (-1 + box[0], 0 + box[1])
    ]

    for i, j in zip(range(0, 4), range(-1, 3)):
      if(self.map[lost_cond[i][0]][lost_cond[i][1]] == "#" and
         self.map[lost_cond[j][0]][lost_cond[j][1]] == "#"):
        return True
    return False

  def lost(self):
    for box in self.boxes:
      if(self._trapped(box)):
        return True
    return False

  def __str__(self):
    local_map = list(map(list, zip(*self.map)))
    res = ""
    for row in local_map:
      for item in row:
        res += str(item)
      res += '\n'
    return res


if __name__ == "__main__":
  game = Game("""####
#-.#
#--###
#*@--#
#--$-#
#--###
####
""")

  while(True):
    direction = input("")
    if direction == "w":
      direction = (0, -1)
    elif direction == "a":
      direction = (-1, 0)
    elif direction == "s":
      direction = (0, 1)
    else:
      direction = (1, 0)

    game.move(direction)
