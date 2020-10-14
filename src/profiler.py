import sys
import os
from time import time
from agent import Agent
import re
last_attempt = []
f = open("./stats.txt", "r").read()
for i in f.split("\n"):
  try:
    info = re.sub(r"\(.*?\)", "", i.split("duration")[1].replace(
        "ms", "").replace("steps", "")).split(":")
    last_attempt.append((int(info[0]), int(info[1])))
  except:
    last_attempt.append(((99999), (9999)))


for i in range(len(last_attempt), 156):
  last_attempt.append(((99999), (9999)))

for i in range(1, 156):
  start_time = time()
  _original_stdout = sys.stdout
  sys.stdout = open(os.devnull, 'w')
  steps = Agent(open(f"levels/{i}.xsb").read()).solve(300)
  sys.stdout.close()
  sys.stdout = _original_stdout
  elapsed_time = time() - start_time
  if(steps != None):
    time_str = "{:>9}".format((str(int(elapsed_time * 1000) % 1000)) + " ") + \
        "({:>9})".format(
        (str((int(elapsed_time * 1000) % 1000) - last_attempt[i][0])) + "ms")
    level_str = "{:<2}".format(i) 
    steps_str = "{:>6}".format(len(steps)) + \
        "({:>6})".format((len(steps) - last_attempt[i][1]))
    print(f"level {level_str} - duration {time_str}:  steps {steps_str}")
  else:
    print(f"level {i} - Timed out")
