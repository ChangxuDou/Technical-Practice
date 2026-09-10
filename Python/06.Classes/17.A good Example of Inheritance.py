class InvalidOperationError(Exception):
    pass


class Stream:
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


class FileStream(Stream):
    def read(self):
        print("Reading data from a file")


class NetworkStream(Stream):
    def read(self):
        print("Reading data from a network")
