"""Module for Library Pipeline Operators."""
from abc import ABC
from numpy.lib.arraysetops import unique
import pandas as pd

class DataSetOperator:
    def __init__(self) -> None:
        pass

    def load(self, **kwargs):
        raise NotImplementedError()

    def preprocess(self, df, **kwargs):
        raise NotImplementedError()

    def split(self, df, **kwargs):
        raise NotImplementedError()


class Pipeline(DataSetOperator):
    def __init__(self) -> None:
        super().__init__()

    def preprocess(self, df, **kwargs):
        df = df.dropna()
        return df

    @classmethod
    def split(cls, df, **kwargs):
        train_df = df.sample(frac=kwargs.get("frac") or 0.8,
                             random_state=kwargs.get("random_state") or 0)
        test_df = df.drop(train_df.index)
        return train_df, test_df

    @classmethod
    def to_dummies(cls, df, feature, **kwargs):
        unique_feature = list(df[feature].unique())
        df[feature] = df[feature].map(dict(enumerate(unique_feature)))
        # df[feature] = df[feature].map({1: 'USA', 2: 'Europe', 3: 'Japan'})
        df = pd.get_dummies(df, columns=[feature], prefix='', prefix_sep='')
        return df

    def prepare_train_test(self, df, y_column):
        train_x, test_x = self.split(df)
        train_y = train_x.pop(y_column)
        test_y = test_x.pop(y_column)
        return train_x, train_y, test_x, test_y