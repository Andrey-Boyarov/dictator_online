import logging
import os
import sys

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine


class DbConnector:
    def __init__(self, timeout=10):
        self._logger = logging.getLogger(__name__)
        self._config = dict()
        self.load_config()
        self._engine = create_async_engine(
            f'postgresql+asyncpg://'
            f'{self._config["DB_USERNAME"]}:{self._config["DB_PASSWORD"]}'
            f'@{self._config["HOST"]}:{self._config["PORT"]}'
            f'/{self._config["DB_DATABASE"]}',
            pool_pre_ping=True,
            connect_args={'timeout': timeout}
        )

    def load_config(self) -> None:
        """
            Производит загрузку переменных из окружения, с помощью которых можно будет подключиться к БД
        """
        try:
            self._logger.info('Загружаем переменные из окружения')
            self._config['HOST'] = os.environ['HOST']
            self._config['PORT'] = os.environ['PORT']
            self._config['DB_USERNAME'] = os.environ['DB_USERNAME']
            self._config['DB_PASSWORD'] = os.environ['DB_PASSWORD']
            self._config['DB_DATABASE'] = os.environ['DB_DATABASE']
        except KeyError as e:
            self._logger.error(f'Невозможно найти ключ {e} в переменных окружения. Завершаем работу программы')
            sys.exit(1)

    def create_async_session(self) -> AsyncSession:
        """
            Создаёт асинхронную сессию с БД
            :return: Асинхронная сессия
        """
        return async_sessionmaker(self._engine, expire_on_commit=False).begin()

    def get_engine(self) -> AsyncEngine:
        """
        :return: Асинхронный движок подключения к БД
        """
        return self._engine
