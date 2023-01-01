#!/usr/bin/env python


class LocalFileException(Exception):
    def __init__(self, arg):
        self.msg = arg

    def __str__(self):
        return self.msg


class LocalTwitterException(Exception):
    def __init__(self, arg):
        self.msg = arg

    def __str__(self):
        return self.msg
