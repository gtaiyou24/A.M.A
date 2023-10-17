from __future__ import annotations

from sqlalchemy import TEXT, Integer, Boolean, String
from sqlalchemy.orm import mapped_column, Mapped

from domain.model.outfit import Outfit
from port.adapter.persistence.repository.mysql import DataBase


class OutfitImagesTableRow(DataBase):
    __tablename__ = "outfit_images"
    __table_args__ = ({"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"})

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    outfit_id: Mapped[str] = mapped_column(String(255), nullable=False)
    image_url: Mapped[str] = mapped_column(TEXT, nullable=False)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    @staticmethod
    def of(outfit: Outfit) -> list[OutfitImagesTableRow]:
        return [OutfitImagesTableRow(outfit_id=outfit.outfit_id.id, image_url=image.address) for image in outfit.images]
