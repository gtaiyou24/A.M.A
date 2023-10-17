from typing import Optional, NoReturn, Any

from injector import inject
from sqlalchemy import Engine
from sqlalchemy.orm import Session, Query

from port.adapter.persistence.repository.mysql.outfit.driver import OutfitsTableRow


class OutfitsCrud:
    @inject
    def __init__(self, engine: Engine):
        self.__engine = engine

    def count(self, gender: Optional[int] = None) -> int:
        with Session(self.__engine, future=True) as session:
            query: Query[OutfitsTableRow] = session.query(OutfitsTableRow)
            if gender is not None:
                query = query.filter_by(gender=gender)
            return query.filter_by(deleted=False).count()

    def find_one_by(self, **kwargs: Any) -> Optional[OutfitsTableRow]:
        with Session(self.__engine, future=True) as session:
            return session.query(OutfitsTableRow).filter_by(**kwargs).one_or_none()

    def pagination(self, gender: Optional[int], start: int, size: int) -> list[OutfitsTableRow]:
        with Session(self.__engine, future=True) as session:
            query: Query[OutfitsTableRow] = session.query(OutfitsTableRow)
            if gender is not None:
                query = query.filter_by(gender=gender)
            return query.filter_by(deleted=False).offset(start).limit(size).all()

    def upsert(self, outfit_table_row: OutfitsTableRow) -> NoReturn:
        optional = self.find_one_by(id=outfit_table_row.id)
        with Session(self.__engine, future=True) as session:
            if optional is None:
                session.add(outfit_table_row)
            else:
                optional.update(outfit_table_row)
            session.commit()

    def delete(self, id: str) -> NoReturn:
        with Session(self.__engine, future=True) as session:
            table_row: OutfitsTableRow = session.query(OutfitsTableRow).get(id)
            table_row.deleted = True
            session.commit()
