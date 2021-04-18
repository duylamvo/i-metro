"""Test Module for Pipeline Operators."""
from libopt.dataset import Pipeline
from libopt.hook import PostgresLocal
from libopt.logger import Logger, PostgresLogger

import pandas as pd
import numpy as np
import pytest

def load_data():
    df = pd.DataFrame({'a': range(10), 'b': range(10), 'c': range(10)})
    return df
                    
def test_preprocessing():
    p = Pipeline()
    df = load_data()
    df = p.preprocess(df)
    assert np.array(df.isna()).sum() == 0

def test_stdout_logger():
    logger = Logger()
    logger.write(a=1, b=2)
    logger.write(a=3, b=5)
    logger.write(a=4, b=6)
    
    assert len(logger.buffer) == 3
    
    logger.publish()
    assert logger.buffer == []

@pytest.mark.skip("Require Local Postgres")
def test_postgres_logger():
    logger = PostgresLogger(table_name = "m_exe_test")
    logger.write(a=1, b=2)
    logger.write(**{'a':3, 'b':5})
    logger.write(a=4, b=6)
    assert len(logger.buffer) == 3
    
    logger.publish(if_exists='replace')
    assert logger.buffer == []
    
    df = pd.read_sql_table(logger.table_name, logger.engine)
    assert len(df.index) == 3
  
    