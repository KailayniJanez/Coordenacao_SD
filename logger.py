import os
import time

class Logger:

    def __init__(self,node):
        os.makedirs("logs",exist_ok=True)
        self.file=f"logs/node{node}.log"

    def log(self,msg):

        line=f"[{time.time()}] {msg}"

        print(line, flush=True)

        with open(self.file,"a") as f:
            f.write(line+"\n")
            f.flush()