import sys
import os
from time import time
from agent import Agent

for i in range(1, 156):
  start_time = time()
  _original_stdout = sys.stdout
  sys.stdout = open(os.devnull, 'w')
  steps = Agent(open(f"levels/{i}.xsb").read()).solve(301000)
  sys.stdout.close()
  sys.stdout = _original_stdout
  elapsed_time = time() - start_time
  if(steps != None):
    time_str = "{:>9}".format((str(int(elapsed_time * 1000) % 1000)) + "ms")
    level_str = "{:<2}".format(i)
    print(f"level {level_str} - duration {time_str} :  steps {len(steps)}")
  else:
    print(f"level {i} - Timed out")