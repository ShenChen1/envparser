#!/usr/bin/env python

import logging
import os
import re
import sys
import io
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class envparser:

    def __init__(self, envpath=None, verbose=False):
        self.__envpath = envpath
        self.__verbose = verbose
        self.__envdict = {}

        # read from envpath
        if envpath:
            self.__parse()

    @contextmanager
    def __get_stream(self):
        if isinstance(self.__envpath, io.StringIO):
            yield self.__envpath
        elif os.path.isfile(self.__envpath):
            with io.open(self.__envpath) as stream:
                yield stream
        else:
            if self.__verbose:
                logger.warning("File doesn't exist %s", self.dotenv_path)
            yield io.StringIO('')

    def __parse(self):
        skip_pattern = re.compile(r"^\s*$")
        skip_pattern1 = re.compile(r"^\#")
        match_pattern = re.compile(r"^(\w+)=(.*)")

        with self.__get_stream() as stream:
            for line in stream.readlines():
                line = line.strip()
                if skip_pattern.match(line):
                    continue
                if skip_pattern1.match(line):
                    continue
                regex = match_pattern.match(line)
                if regex is None:
                    continue
                (k, v) = regex.groups()
                self.set(k, v, True)
        if self.__verbose:
            self.dump()

    def set(self, key, val=None, override=False):
        if key in self.__envdict and val and not override:
            return False

        if val is not None:
            self.__envdict[key] = val
            if self.__verbose:
                logger.info("Add %s = %s.", key, val)
        else:
            if self.__verbose:
                logger.info("Del %s = %s.", key, self.__envdict[key])
            del self.__envdict[key]

        return True

    def get(self, key, default=None):
        if key in self.__envdict:
            return self.__envdict[key]

        return default

    def dump(self):
        logger.info("\n======== ENV ========")
        for k, v in self.__envdict.items():
            logger.info("%s = %s", k, v)
        logger.info("=====================\n")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    env = envparser("./demo", True)
    env.set("hostname", "demo")
    env.dump()
    logger.info("hostname = %s", env.get("hostname", "mine"))
    logger.info("aaa = %s", env.get("aaa", "bbb"))
    env.set("hostname")
    env.dump()
