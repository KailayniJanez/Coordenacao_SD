import socket
import json
import time

class Heartbeat:

    def send(self,nodes,node_id):

        while True:

            for n in nodes:

                if n != node_id:

                    try:

                        s = socket.socket()

                        s.settimeout(1)

                        s.connect(
                            (
                                f"node{n}",
                                5000+n
                            )
                        )

                        msg = {

                            "type":"heartbeat",

                            "leader":node_id,

                            "timestamp":time.time()

                        }

                        s.send(
                            json.dumps(
                                msg
                            ).encode()
                        )

                        s.close()

                    except:
                        pass

            time.sleep(1)