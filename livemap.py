

class liveMap:
    def __init__(self, filename):
        self._map= []
        with open(filename, "r") as f:
            i = 0
            j = 0
            for line in f:
                j += len(line.rstrip())
                self._map.append([list(line.rstrip())])
                i += 1
    
        #for i, row in enumerate(mapa):
            #for j, elem in enumerate(row):
                #val = elem
                #if val == "#":
                #    val = "W"
                #elif val == '-':
                #    val = " "
                #elif val == '*':
                #    val = "D"
                #elif val == '@':
                #    val = "P"
                #elif val == '$':
                #    val = "B"
                #self._map[i][j] = val
    
    def getMap(self):
        return self._map
    
    def __str__(self):
        res = ""
        for row in self._map:
            res += str(row) + '\n'
        return res


    def move(self, dir):
        pos = keeper()
        x_dir, y_dir = dir
        if can_move(pos, dir):
            if get_tile(pos + dir) == TILES.BOX:
                sset_tile(pos + 2 * dir, TILES.BOX)
            set_tile(pos, self._originalmap.get_tile(pos))
            set_tile(pos + dir, TILES.MAN)
    
    def can_move(self, pos, dir):
        xi, yi = pos
        x_dir, y_dir = dir
        x, y = (xi + x_dir, yi + y_dir)
        if x not in range(self.hor_tiles) or y not in range(self.ver_tiles):
            logger.error("Position out of map")
            return True
        if self.curr_map[y][x] == '#':
            logger.debug("Position is a wall")
            return True
        if self.curr_map[x][y] == '' and can_move((x, y), dir):
            logger.debug("Against the box there's a wall")
            return True
        return False

    def keeper():
        return self._keeper
        
