from abc import ABC, abstractmethod


class InvalidOperationError(Exception):
    pass


class Stream(ABC):
    def __init__(self):
        self.open = False

    def open(self):
        if open(self):
            raise InvalidOperationError("Stream is already open")
        self.open = True

    def close(self):
        if not open(self):
            raise InvalidOperationError("Stream is already closed")
        self.open = False

    @abstractmethod
    def read(self):
        pass


class FileStream(Stream):
    def read(self):
        print("Reading data from a file")


class NetworkStream(Stream):
    def read(self):
        print("Reading data from a network")


class Memotystream(Stream):
    def read(self):
        print("Reading data from a memory stream")


stream = Memotystream()
stream.read()
