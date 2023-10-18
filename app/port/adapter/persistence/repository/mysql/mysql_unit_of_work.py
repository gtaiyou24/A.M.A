from __future__ import annotations

from typing import NoReturn, Optional

from sqlalchemy import Engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from application import UnitOfWork


class MySQLUnitOfWork(UnitOfWork):
    instance: Optional[MySQLUnitOfWork] = None

    def __init__(self, engine: Engine, session: Session):
        self.__engine = engine
        self.__session = session

    @staticmethod
    def current(engine: Optional[Engine] = None) -> MySQLUnitOfWork:
        if MySQLUnitOfWork.instance is None:
            MySQLUnitOfWork.instance = MySQLUnitOfWork(
                engine,
                scoped_session(sessionmaker(bind=engine))()
            )
        return MySQLUnitOfWork.instance

    def session(self) -> Session:
        return self.__session

    def start(self) -> NoReturn:
        self.__session.begin()

    def rollback(self) -> NoReturn:
        self.__session.rollback()
        self.__session.close()
        self.instance = None

    def commit(self) -> NoReturn:
        self.__session.commit()
        self.__session.close()
        self.instance = None
