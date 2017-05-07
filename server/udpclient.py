import socket
import sys

import logger


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    logger.notice("UDP Socket " + str(s.getsockname()) + "established")
    for data in sys.stdin:
        s.sendto(data.encode(), ('127.0.0.1', 20000))

    logger.notice("Closing UDP socket " + str(s.getsockname()))
    s.close()


if __name__ == '__main__':
    main()
