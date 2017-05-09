import datetime
import sys


def error(msg):
    sys.stderr.write(str(datetime.datetime.now()) + ' [ERR!] ' + str(msg) + '\n')
    sys.stderr.flush()


def warning(msg):
    sys.stderr.write(str(datetime.datetime.now()) + ' [WARN] ' + str(msg) + '\n')
    sys.stderr.flush()


def notice(msg):
    sys.stderr.write(str(datetime.datetime.now()) + ' [NOTI] ' + str(msg) + '\n')
    sys.stderr.flush()


def info(msg):
    sys.stdout.write(str(datetime.datetime.now()) + ' [INFO] ' + str(msg) + '\n')
    sys.stdout.flush()


def debug(msg):
    sys.stdout.write(str(datetime.datetime.now()) + ' [DBG ] ' + str(msg) + '\n')
    sys.stdout.flush()
