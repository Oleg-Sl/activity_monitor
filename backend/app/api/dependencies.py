from typing import Annotated
from fastapi import Depends

from app.utils.unitofwork import UnitOfWork, IUnitOfWork
from app.bitrix24.bitrix_client import InterfaceBitrixClient

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]

# BXClient = Annotated[InterfaceBitrixClient, Depends()]
