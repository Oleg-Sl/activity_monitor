from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def add_one(self, data: dict):
        pass

    @abstractmethod
    async def find_all(self):
        pass
