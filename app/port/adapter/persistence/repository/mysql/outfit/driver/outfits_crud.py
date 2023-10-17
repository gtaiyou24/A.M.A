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

    def insert(self, table_row: OutfitsTableRow) -> NoReturn:
        with Session(self.__engine, future=True) as session:
            session.add(table_row)
            session.commit()

    def update(self, table_row: OutfitsTableRow) -> NoReturn:
        optional = self.find_one_by(id=table_row.id)
        if optional is None:
            raise Exception(f'コーディネート {table_row.id} がないため、更新できません。')
        with Session(self.__engine, future=True) as session:
            optional.update(table_row)
            session.commit()

    def upsert(self, table_row: OutfitsTableRow) -> NoReturn:
        optional = self.find_one_by(id=table_row.id)
        with Session(self.__engine, future=True) as session:
            if optional is None:
                session.add(table_row)
            else:
                optional.update(table_row)
            session.commit()

    def delete(self, id: str) -> NoReturn:
        with Session(self.__engine, future=True) as session:
            table_row: OutfitsTableRow = session.query(OutfitsTableRow).get(id)
            table_row.deleted = True
            session.commit()
