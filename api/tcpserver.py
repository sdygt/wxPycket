import os
from socketserver import StreamRequestHandler, ThreadingTCPServer

from logger import logger


class MainTCPHandler(StreamRequestHandler):
    def __init__(self, request, client_address, server):
        StreamRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        logger.notice("New connection from " + str(self.client_address))

        while os.path.isfile('.enable'):
            msg = self.request.recv(8192)
            logger.info(str(self.client_address) + " " +str(msg))
            if not msg:
                break

        logger.notice("Disconnected from " + str(self.client_address))


if __name__ == '__main__':
    serv = ThreadingTCPServer(('', 20000), MainTCPHandler)

    print("Listening on TCP Port " + str(serv.server_address))
    serv.serve_forever()
