"""Hook for constant setting to connect databases."""
from sqlalchemy import create_engine


class Hook:
    def __init__(self,
                 db_engine='', dialect='',
                 host='', port='',
                 user='', password='', db=''
                 ) -> None:
        self._engine_str = f'{db_engine}+{dialect}://{user}:{password}@{host}:{port}/{db}'
        self.engine = create_engine(self._engine_str)


class PostgresLocal(Hook):
    def __init__(self, host='localhost', port='5432',
                 user='postgres', password='postgres', db='postgres') -> None:
        super().__init__('postgresql', 'psycopg2', host, port, user, password, db)
