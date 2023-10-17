from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, func, TEXT, VARCHAR, Integer, Boolean
from sqlalchemy.orm import Mapped

from domain.model.image import Image
from domain.model.outfit import Outfit, Gender, OutfitId
from domain.model.url import URL
from port.adapter.persistence.repository.mysql import DataBase
from port.adapter.persistence.repository.mysql.outfit.driver import OutfitImagesTableRow


class InterestGender:
    VALUES = {Gender.WOMEN.value: 0, Gender.MEN.value: 1, Gender.KIDS.value: 2, Gender.UNKNOWN.value: 3}

    @staticmethod
    def integer(gender: Gender) -> int:
        return InterestGender.VALUES.get(gender.value)

    @staticmethod
    def domain_object(gender: int) -> Gender:
        genders = [k for k, v in InterestGender.VALUES.items() if v == gender]
        if genders:
            return Gender(genders[0])
        raise Exception(f'outfits.gender = {gender} に該当する Gender オブジェクトが見つかりません')


class OutfitsTableRow(DataBase):
    __tablename__ = "outfits"
    __table_args__ = ({"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"})

    id: Mapped[str] = Column('id', VARCHAR(255), primary_key=True, nullable=False)
    gender: Mapped[int] = Column('gender', Integer, nullable=False, comment='0: WOMEN, 1: MEN, 2: KIDS, 3: UNKNOWN')
    description: Mapped[str] = Column('description', TEXT, nullable=False)
    posted_at: Mapped[datetime] = Column('posted_at', DateTime(timezone=True), nullable=True)
    url: Mapped[str] = Column('url', TEXT, nullable=False)
    created_at: Mapped[datetime] = Column('created_at', DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = Column('updated_at', DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted: Mapped[bool] = Column('deleted', Boolean, default=False)

    def update(self, new_table_row: OutfitsTableRow):
        self.gender = new_table_row.gender
        self.description = new_table_row.description
        self.posted_at = new_table_row.posted_at
        self.url = new_table_row.url

    @staticmethod
    def of(outfit: Outfit) -> OutfitsTableRow:
        return OutfitsTableRow(
            id=outfit.outfit_id.id,
            gender=InterestGender.integer(outfit.gender),
            description=outfit.description,
            posted_at=outfit.posted_at,
            url=outfit.url.address
        )

    def to_entity(self, outfit_images_table_rows: list[OutfitImagesTableRow]) -> Outfit:
        return Outfit(
            OutfitId(self.id),
            InterestGender.domain_object(self.gender),
            [Image(table_row.image_url) for table_row in outfit_images_table_rows],
            self.description,
            self.posted_at,
            URL(self.url)
        )
