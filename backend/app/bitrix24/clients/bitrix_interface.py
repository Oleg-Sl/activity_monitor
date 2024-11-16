from abc import ABC, abstractmethod


class InterfaceBitrixClient(ABC):
    @abstractmethod
    async def call(self, method: str, data: dict, count: int = None) -> dict:
        raise NotImplementedError
    
    @abstractmethod
    async def batch(self, data: dict) -> dict:
        raise NotImplementedError
