from socketserver import BaseRequestHandler, ThreadingTCPServer

from logger import logger


class MainHandler(BaseRequestHandler):
    def handle(self):
        logger.notice("New connection from " + str(self.client_address))
        while True:
            msg = self.request.recv(8192)
            logger.info(msg)
            if not msg:
                break

        logger.notice("Disconnected from " + str(self.client_address))


if __name__ == '__main__':
    serv = ThreadingTCPServer(('', 20000), MainHandler)

    print("Listening on TCP Port " + str(serv.server_address))
    serv.serve_forever()
