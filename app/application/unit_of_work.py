from __future__ import annotations

import abc
from typing import NoReturn, Optional

from sqlalchemy import Engine


class UnitOfWork(abc.ABC):
    @abc.abstractmethod
    def start(self) -> NoReturn:
        """トランザクションを開始する"""
        pass

    @abc.abstractmethod
    def rollback(self) -> NoReturn:
        """ロールバックする"""
        pass

    @abc.abstractmethod
    def commit(self) -> NoReturn:
        """トランザクションをコミットする"""
        pass
