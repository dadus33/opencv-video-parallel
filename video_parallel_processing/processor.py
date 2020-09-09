import abc
from abc import ABCMeta


class Processor(metaclass=ABCMeta):
    @abc.abstractmethod
    def __init__(self, process_index, metadata):
        self.process_index = process_index
        self.metadata = metadata

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @abc.abstractmethod
    def process(self, frame, current_frame):
        pass
