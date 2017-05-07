from socketserver import BaseRequestHandler, TCPServer

from logger import logger


class MainHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        while True:

            msg = self.request.recv(8192)
            if not msg:
                break
            self.request.send(msg)


if __name__ == '__main__':
    serv = TCPServer(('', 20000), MainHandler)
    logger.error('dassd')
    print("Listening on TCP Port " + str(serv.server_address))
    serv.serve_forever()
