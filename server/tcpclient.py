import socket
import sys

from logger import logger


def main():
    PORT = ('127.0.0.1', 20000)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(PORT)
    logger.notice("TCP Connection " + str(s.getsockname()) + " established")
    for data in sys.stdin:
        s.send(data.encode())

    logger.notice("Closing TCP Connection " + str(s.getsockname()))
    s.close()


if __name__ == '__main__':
    main()
