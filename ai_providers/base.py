from abc import ABC, abstractmethod


class AIProvider(ABC):

    @abstractmethod
    def generate_script(self, topic: str, duration: int) -> str:
        pass
