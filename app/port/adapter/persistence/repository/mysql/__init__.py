from sqlalchemy.orm import declarative_base

DataBase = declarative_base()

from .mysql_unit_of_work import MySQLUnitOfWork
