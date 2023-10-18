from typing import NoReturn, Optional

from injector import singleton, inject
from sqlalchemy import Engine

from application import UnitOfWork
from port.adapter.persistence.repository.mysql import MySQLUnitOfWork


@singleton
class ApplicationServiceLifeCycle:
    @inject
    def __init__(self, engine: Engine):
        self.__engine = engine

    def begin(self, is_listening: bool = True) -> NoReturn:
        if is_listening:
            self.listen()
        MySQLUnitOfWork.current(self.__engine).start()

    def fail(self, exception: Optional[Exception] = None) -> NoReturn:
        MySQLUnitOfWork.current().rollback()
        if exception is not None:
            raise exception

    def success(self) -> NoReturn:
        MySQLUnitOfWork.current().commit()

    def listen(self) -> NoReturn:
        pass
