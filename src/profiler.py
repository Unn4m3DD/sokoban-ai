import sys
import os
from time import time
from agent import Agent
import re
import json
last_attempt = [None]
f = open("./stats.txt", "r").read()
for i in f.split("\n")[:-1]:
  try:
    info = re.sub(r"\(.*?\)", "", i.split("duration")[1].replace(
        "ms", "").replace("steps", "")).split(":")
    last_attempt.append((int(info[0]), int(info[1])))
  except:
    last_attempt.append(((99999), (9999)))


try:
  last_attempt_info = json.loads(f.split("\n")[-1])
except:
  last_attempt_info = {
      "beaten": 0,
      "avg time[ms]": 99999,
      "max time[ms]": 99999,
      "min time[ms]": 99999,
      "avg steps": 99999,
      "max steps": 99999,
      "min steps": 99999
  }
for i in range(len(last_attempt), 156):
  last_attempt.append(((99999), (9999)))

current_attempt = [None]

for i in range(1, 156):
  start_time = time()
  _original_stdout = sys.stdout
  sys.stdout = open(os.devnull, 'w')
  steps = Agent(open(f"levels/{i}.xsb").read()).solve(300)
  sys.stdout.close()
  sys.stdout = _original_stdout
  #print(">>", steps, "<<")
  elapsed_time = time() - start_time
  if(steps != None):
    current_attempt.append((int(elapsed_time * 1000), len(steps)))
    time_str = "{:>9}".format((str(int(elapsed_time * 1000))) + " ") + \
        "({:>9})".format(
        (str((int(elapsed_time * 1000)) - last_attempt[i][0])))
    level_str = "{:<2}".format(i)
    steps_str = "{:>6}".format(len(steps)) + \
        "({:>6})".format((len(steps) - last_attempt[i][1]))
    print(f"level {level_str} - duration[ms] {time_str}:  steps {steps_str}")
  else:
    current_attempt.append(None)
    print(f"level {i} - Timed out")

times = [i[0] for i in current_attempt if i is not None]
stepss = [i[1] for i in current_attempt if i is not None]
beaten = [i for i in current_attempt if i is not None]

info = {
    "beaten": len(beaten),
    "avg time[ms]": int(sum(times)/len(times)),
    "max time[ms]": max(times),
    "min time[ms]": min(times),
    "avg steps": int(sum(stepss)/len(stepss)),
    "max steps": max(stepss),
    "min steps": min(stepss),
    "diff beaten": len(beaten) - last_attempt_info["beaten"],
    "diff avg time[ms]":  int(sum(times)/len(times)) - last_attempt_info["avg time[ms]"],
    "diff max time[ms]":  max(times) - last_attempt_info["max time[ms]"],
    "diff min time[ms]":  min(times) - last_attempt_info["min time[ms]"],
    "diff avg steps": int(sum(stepss)/len(stepss)) - last_attempt_info["avg steps"],
    "diff max steps": max(stepss) - last_attempt_info["max steps"],
    "diff min steps": min(stepss) - last_attempt_info["min steps"],
}
print(json.dumps(info))
