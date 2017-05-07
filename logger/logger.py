import datetime
import sys


def error(msg):
    sys.stderr.write(str(datetime.datetime.now()) + ' [ERR!] ' + msg)


def warning(msg):
    sys.stderr.write(str(datetime.datetime.now()) + ' [WARN] ' + msg)


def notice(msg):
    sys.stderr.write(str(datetime.datetime.now()) + ' [NOTI] ' + msg)


def info(msg):
    sys.stdout.write(str(datetime.datetime.now()) + ' [INFO] ' + msg)


def debug(msg):
    sys.stdout.write(str(datetime.datetime.now()) + ' [DBG ] ' + msg)
