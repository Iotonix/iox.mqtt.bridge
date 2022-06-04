from abc import ABCMeta, abstractmethod


class BridgeInterface:
    """As per conventions a plugin need to derrive from BridgeInterface
    base class
    Please note that this is untested and only from my memory :-)
    Please remove this comment once this is working in any shape or form"""

    __metaclass__ = ABCMeta

    @classmethod
    def version(cls):
        return "1.0"

    @abstractmethod
    def transform(self):
        raise NotImplementedError

    @abstractmethod
    def terminate(self):
        raise NotImplementedError
