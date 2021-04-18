"""Logger Module for recording executions."""
from .hook import PostgresLocal

import pandas as pd

class AbstractLogger:
    """Abstract module for logger."""
    def __init__(self, **kwargs) -> None:
        self.buffer = list()    # list of events (dicts)
    
    def write(self, **kwargs):
        raise NotImplementedError()
    
    def clear_buffer(self, **kwargs):
        raise NotImplementedError()
    
    def publish(self, **kwargs):
        raise NotImplementedError()
    

class Logger(AbstractLogger):
    """Local Logger for stout."""
    def write(self, **kwargs):
        self.buffer.append(kwargs)
        
    def clear_buffer(self, **kwargs):
        self.buffer = list()
        
    def publish(self, **kwargs):
        df = pd.DataFrame(self.buffer)
        print(df)
        self.clear_buffer()

class PostgresLogger(Logger):
    """Logger to import to Postgres."""
    def __init__(self, table_name, **kwargs) -> None:
        super().__init__(**kwargs)
        self.engine = PostgresLocal().engine
        self.table_name = table_name
       
    def publish(self, **kwargs):
        df = pd.DataFrame(self.buffer)
        df.to_sql(self.table_name, self.engine, index=False, **kwargs)
        self.clear_buffer()