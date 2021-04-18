"""Test for auto mpg pipeline."""
from libopt.dataset import Pipeline
from libopt.model import LinearModel, DNNModel
from libopt.hook import PostgresLocal
from libopt.logger import Logger

import pandas as pd
import numpy as np

def load_data():
    url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data'    
    column_names = ['MPG', 'Cylinders', 'Displacement', 
                    'Horsepower', 'Weight', 'Acceleration', 
                    'Model_Year', 'Origin'
                    ]
    column_names = [c.lower() for c in column_names]

    df = pd.read_csv(url, names=column_names,
                    na_values='?', comment='\t',
                    sep=' ', skipinitialspace=True)
    return df

def import_to_postgres():
    df = load_data()
    df.to_sql('auto_mpg_test', PostgresLocal().engine, if_exists='replace', index=False)   

def test_sql_query():
    df = pd.read_sql_table('auto_mpg_test', PostgresLocal().engine)   
    p = Pipeline()
    df = p.preprocess(df)
    assert np.array(df.isna()).sum() == 0
    
def test_model_train():
    p = Pipeline()
    df = load_data()
    df = p.preprocess(df)
    
    # Custom for data set mpg only
    df['origin'] = df['origin'].map({1: 'USA', 2: 'Europe', 3: 'Japan'})
    df = pd.get_dummies(df, columns=['origin'], prefix='', prefix_sep='')
    train_x, train_y, test_x, test_y = p.prepare_train_test(df, y_column='mpg')
    assert len(train_x.index) > 0
    
    logger = Logger()
    
    ln = LinearModel()
    _ = ln.train(train_x, train_y)  
    eval_result = ln.eval(test_x, test_y)
    assert isinstance(eval_result, float)
    
    logger.write(**ln.metadata)
    
    dnn = DNNModel()
    _ = dnn.train(train_x, train_y, verbose=0)
    eval_result = dnn.eval(test_x, test_y, verbose=0)
    assert isinstance(eval_result, float)

    logger.write(**dnn.metadata)
    
    # from datetime import datetime
    # datetime.fromtimestamp(dnn.metadata.get("trained_on"))
    logger.publish()