import socket
import json

class BullyElection:

    def __init__(self, node_id, nodes, logger):

        self.id = node_id
        self.nodes = nodes
        self.logger = logger


    def start(self):

        self.logger.log("Iniciando eleição")

        # procura IDs maiores que o atual
        higher = [
            n for n in self.nodes
            if n > self.id
        ]

        answered = False

        for node in higher:

            try:

                s = socket.socket()

                s.settimeout(2)

                s.connect(
                    (
                        f'node{node}',
                        5000 + node
                    )
                )

                msg = {
                    'type':'election'
                }

                s.send(
                    json.dumps(msg).encode()
                )

                response = s.recv(1024)

                if response:

                    data = json.loads(
                        response.decode()
                    )

                    if data['type']=='ok':

                        self.logger.log(
                        f"Nó {node} respondeu"
                        )

                        answered=True

                s.close()

            except:

                self.logger.log(
                f"Nó {node} indisponível"
                )


        if not answered:

            self.logger.log(
            "Sou novo líder"
            )

            return True

        return False