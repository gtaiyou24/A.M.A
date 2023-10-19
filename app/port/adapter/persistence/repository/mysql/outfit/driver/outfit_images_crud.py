from typing import Any, NoReturn

from injector import inject
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from application import UnitOfWork
from port.adapter.persistence.repository.mysql import MySQLUnitOfWork
from port.adapter.persistence.repository.mysql.outfit.driver import OutfitImagesTableRow


class OutfitImagesCrud:
    @inject
    def __init__(self, unit_of_work: UnitOfWork):
        self.__unit_of_work: MySQLUnitOfWork = unit_of_work

    def find_all_by(self, **kwargs: Any) -> list[OutfitImagesTableRow]:
        with self.__unit_of_work.query() as session:
            return session.query(OutfitImagesTableRow).filter_by(**kwargs).all()

    def insert(self, table_rows: list[OutfitImagesTableRow]) -> NoReturn:
        self.__unit_of_work.transaction().add_all(table_rows)

    def delete(self, **kwargs) -> NoReturn:
        self.__unit_of_work.transaction().query(OutfitImagesTableRow).filter_by(**kwargs).delete()
