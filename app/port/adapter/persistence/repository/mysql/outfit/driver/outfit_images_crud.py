from typing import Any, NoReturn

from injector import inject
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from port.adapter.persistence.repository.mysql import MySQLUnitOfWork
from port.adapter.persistence.repository.mysql.outfit.driver import OutfitImagesTableRow


class OutfitImagesCrud:
    @inject
    def __init__(self, engine: Engine):
        self.__engine = engine

    def find_all_by(self, **kwargs: Any) -> list[OutfitImagesTableRow]:
        with Session(bind=self.__engine) as session:
            return session.query(OutfitImagesTableRow).filter_by(**kwargs).all()

    def insert(self, table_rows: list[OutfitImagesTableRow]) -> NoReturn:
        MySQLUnitOfWork.current().session().add_all(table_rows)

    def delete(self, **kwargs) -> NoReturn:
        MySQLUnitOfWork.current().session().query(OutfitImagesTableRow).filter_by(**kwargs).delete()
