from abc import ABCMeta, abstractmethod


class SimulatorInterface:
    """As per conventions a simulator needs to derrive from SimulatorInterface
    base class"""

    __metaclass__ = ABCMeta

    @classmethod
    def version(cls):
        return "1.0"

    @abstractmethod
    def simulate(self, iteration):
        raise NotImplementedError

    @abstractmethod
    def terminate(self):
        raise NotImplementedError
