import socket
import threading
import json
import time
import os
import random

from heartbeat import Heartbeat
from election import BullyElection
from adaptive_timeout import AdaptiveTimeout
from logger import Logger


NODE_ID = int(os.environ["NODE_ID"])
PORT = int(os.environ["PORT"])

nodes = [1,2,3,4]

leader = max(nodes)

last_heartbeat = time.time()

logger = Logger(NODE_ID)
adapt = AdaptiveTimeout()


clock_drift = random.uniform(-0.12,0.12)
start = time.time()


logger.log("======================")
logger.log(f"Nó {NODE_ID} iniciado")
logger.log(f"Porta: {PORT}")
logger.log(f"Líder inicial: {leader}")
logger.log(f"Clock drift: {clock_drift}")


def local_time():

    elapsed = time.time()-start

    return time.time() + elapsed*clock_drift



def server():

    global last_heartbeat
    global leader

    s = socket.socket()

    s.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    s.bind(("",PORT))

    s.listen()

    while True:

        conn,_ = s.accept()

        try:

            data = conn.recv(1024)

            if not data:
                continue

            msg = json.loads(
                data.decode()
            )


            if msg["type"]=="heartbeat":

                last_heartbeat=time.time()

                old=leader

                leader=msg["leader"]

                sample=(
                    time.time()
                    -msg["timestamp"]
                )

                adapt.update(sample)

                if old!=leader:

                    logger.log(
                    f"Novo líder: {leader}"
                    )

                logger.log(
                f"heartbeat líder={leader}"
                )


            elif msg["type"]=="election":

                logger.log(
                "Recebeu eleição"
                )

                response={

                    "type":"ok"

                }

                conn.send(
                    json.dumps(
                        response
                    ).encode()
                )

        except Exception as e:

            logger.log(
            f"Erro: {e}"
            )

        finally:

            conn.close()



threading.Thread(
    target=server,
    daemon=True
).start()


if NODE_ID==leader:

    threading.Thread(
        target=Heartbeat().send,
        args=(nodes,NODE_ID),
        daemon=True
    ).start()



while True:

    timeout = adapt.get_timeout()

    if NODE_ID!=leader:

        if time.time()-last_heartbeat>timeout:

            logger.log(
            "Líder falhou"
            )

            election=BullyElection(
                NODE_ID,
                nodes,
                logger
            )

            won=election.start()

            if won:

                leader=NODE_ID

                last_heartbeat=time.time()

                logger.log(
                "Sou novo líder"
                )

                threading.Thread(
                    target=Heartbeat().send,
                    args=(nodes,NODE_ID),
                    daemon=True
                ).start()

    time.sleep(1)
