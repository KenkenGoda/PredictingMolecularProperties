import os

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold

from .model import LGBMRegressor, LogisticRegression
from .tune import ParameterTuning


class SubTargetPrediction:
    def __init__(self, config):
        self.config = config
        self.pickled_feature_dir = config.pickled_feature_dir
        self.target_name = config.target_name
        self.tuning = config.tuning
        self.n_splits = config.n_splits
        self.save = config.save
        self.seed = config.seed

    def run(self, X_train, y_train, X_test):
        pt = ParameterTuning(self.config)
        if self.tuning is True:
            params = pt.run(X_train, y_train)
        else:
            params = pt.get_best_params()
            if params is None:
                params = {}
        del pt

        kf = KFold(n_splits=self.n_splits, shuffle=True, random_state=self.seed)
        score = []
        y_pred = []
        for train_idx, valid_idx in kf.split(X_train):
            X_train_ = X_train.iloc[train_idx]
            y_train_ = y_train.iloc[train_idx][self.target_name]
            X_valid_ = X_train.iloc[valid_idx]
            y_valid_ = y_train.iloc[valid_idx]
            model = LGBMRegressor(**params)
            model.fit(
                X_train_,
                y_train_,
                eval_set=(X_valid_, y_valid_[self.target_name]),
                early_stopping_rounds=3,
                verbose=500,
            )
            y_pred_ = model.predict(X_valid_)
            score.append(model.calculate_score(y_valid_, y_pred_))
            y_pred.append(model.predict(X_test))
            del X_train_, y_train_, X_valid_, y_valid_, model

        print(f"Score: {np.mean(score)}")
        y_pred = np.mean(y_pred, axis=0)

        if self.save is True:
            self._save_predicted_feature(y_pred, X_test.index)

        return y_pred

    def _save_predicted_feature(self, y_pred, index):
        predicted_feature = pd.DataFrame(y_pred, index=index)
        predicted_feature.columns = [self.target_name]
        path = os.path.join(self.pickled_feature_dir, "test", f"{self.target_name}.pkl")
        predicted_feature.to_pickle(path)
        print(f"save {self.target_name} for test to pickle")


class TargetPrediction:
    def __init__(self, config):
        self.params = config.lr_params

    def run(self, X_train, y_train, X_test):
        model = LogisticRegression(**self.params)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        return y_pred
