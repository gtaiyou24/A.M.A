from typing import Optional, NoReturn, Any

from injector import inject
from sqlalchemy import Engine
from sqlalchemy.orm import Query, Session

from port.adapter.persistence.repository.mysql import MySQLUnitOfWork
from port.adapter.persistence.repository.mysql.outfit.driver import OutfitsTableRow


class OutfitsCrud:
    @inject
    def __init__(self, engine: Engine):
        self.__engine = engine

    def count(self, gender: Optional[int] = None) -> int:
        with Session(bind=self.__engine) as session:
            query: Query[OutfitsTableRow] = session.query(OutfitsTableRow)
            if gender is not None:
                query = query.filter_by(gender=gender)
            return query.filter_by(deleted=False).count()

    def find_one_by(self, **kwargs: Any) -> Optional[OutfitsTableRow]:
        with Session(bind=self.__engine) as session:
            return session.query(OutfitsTableRow).filter_by(**kwargs).one_or_none()

    def pagination(self, gender: Optional[int], start: int, size: int) -> list[OutfitsTableRow]:
        with Session(bind=self.__engine) as session:
            query: Query[OutfitsTableRow] = session.query(OutfitsTableRow)
            if gender is not None:
                query = query.filter_by(gender=gender)
            return query.filter_by(deleted=False).offset(start).limit(size).all()

    def insert(self, table_row: OutfitsTableRow) -> NoReturn:
        MySQLUnitOfWork.current().session().add(table_row)

    def update(self, table_row: OutfitsTableRow) -> NoReturn:
        optional = MySQLUnitOfWork.current().session().query(OutfitsTableRow).filter_by(id=table_row.id).one_or_none()
        if optional is None:
            raise Exception(f'コーディネート {table_row.id} がないため、更新できません。')
        optional.gender = table_row.gender
        optional.description = table_row.description
        optional.posted_at = table_row.posted_at
        optional.url = table_row.url

    def upsert(self, table_row: OutfitsTableRow) -> NoReturn:
        optional = self.find_one_by(id=table_row.id)
        if optional is None:
            self.insert(table_row)
        else:
            self.update(table_row)

    def delete_by(self, **kwargs: Any) -> NoReturn:
        table_row: OutfitsTableRow = MySQLUnitOfWork.current().session().query(OutfitsTableRow).filter_by(**kwargs).one()
        table_row.deleted = True
