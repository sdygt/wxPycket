from socketserver import BaseRequestHandler, ThreadingUDPServer

from logger import logger


class MainHandler(BaseRequestHandler):
    def handle(self):
        msg, sock = self.request
        logger.info("UDP datagram from " + str(self.client_address) + ": " + msg.decode())


if __name__ == '__main__':
    PORT = ('', 20000)
    serv = ThreadingUDPServer(PORT, MainHandler)
    serv.serve_forever()
