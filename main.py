import time
starttime=time.time()
while True:
  print("tick")
  time.sleep(2 - ((time.time() - starttime) % 2))
