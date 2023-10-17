from typing import Any, NoReturn

from injector import inject
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from port.adapter.persistence.repository.mysql.outfit.driver import OutfitImagesTableRow


class OutfitImagesCrud:
    @inject
    def __init__(self, engine: Engine):
        self.__engine = engine

    def find_all_by(self, **kwargs: Any) -> list[OutfitImagesTableRow]:
        with Session(self.__engine, future=True) as session:
            return session.query(OutfitImagesTableRow).filter_by(**kwargs).all()

    def insert(self, table_rows: list[OutfitImagesTableRow]) -> NoReturn:
        with Session(self.__engine, future=True) as session:
            for table_row in table_rows:
                session.add(table_row)
            session.commit()

    def delete(self, **kwargs) -> NoReturn:
        with Session(self.__engine, future=True) as session:
            table_rows: list[OutfitImagesTableRow] = session.query(OutfitImagesTableRow).filter_by(**kwargs).all()
            [session.delete(table_row) for table_row in table_rows]
