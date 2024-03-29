import os

from .param_space import IntParamSpace, UniformParamSpace, LogUniformParamSpace


class Config:
    def __init__(self):
        # raw data path
        self.data_dir = "../data"
        self.train_path = os.path.join(self.data_dir, "train.csv")
        self.test_path = os.path.join(self.data_dir, "test.csv")
        self.sample_submission_path = os.path.join(
            self.data_dir, "sample_submission.csv"
        )
        self.dipole_moments_path = os.path.join(self.data_dir, "dipole_moments.csv")
        self.magnetic_shielding_tensors_path = os.path.join(
            self.data_dir, "magnetic_shielding_tensors.csv"
        )
        self.mulliken_charges_path = os.path.join(self.data_dir, "mulliken_charges.csv")
        self.potential_energy_path = os.path.join(self.data_dir, "potential_energy.csv")
        self.scalar_coupling_contributions_path = os.path.join(
            self.data_dir, "scalar_coupling_contributions.csv"
        )
        self.structures_path = os.path.join(self.data_dir, "structures.csv")

        # pickled files path
        self.pickle_dir = "../pickle"
        self.pickled_data_dir = os.path.join(self.pickle_dir, "data")
        self.pickled_feature_dir = os.path.join(self.pickle_dir, "feature")
        self.pickled_train_path = os.path.join(self.pickled_data_dir, "train.pkl")
        self.pickled_test_path = os.path.join(self.pickled_data_dir, "test.pkl")
        self.pickled_structures_path = os.path.join(
            self.pickled_data_dir, "structures.pkl"
        )

        # submission file path
        self.submission_path = "../results/submission.csv"

        # used feature names
        self.feature_names = [
            "MoleculeType",
            "MoleculeType0",
            "Atom0",
            "Atom1",
            "AtomX0",
            "AtomX1",
            "AtomY0",
            "AtomY1",
            "AtomZ0",
            "AtomZ1",
            "MoleculeDistance",
            "MoleculeDistanceX",
            "MoleculeDistanceY",
            "MoleculeDistanceZ",
            "MoleculeCount",
            "MoleculeX0Statistics",
            "MoleculeX1Statistics",
            "MoleculeY0Statistics",
            "MoleculeY1Statistics",
            "MoleculeZ0Statistics",
            "MoleculeZ1Statistics",
            "MoleculeDistanceStatistics",
            "MoleculeDistanceXStatistics",
            "MoleculeDistanceYStatistics",
            "MoleculeDistanceZStatistics",
            "Atom0Count",
            "Atom1Count",
            "Atom0X1Statistics",
            "Atom1X0Statistics",
            "Atom0Y1Statistics",
            "Atom1Y0Statistics",
            "Atom0Z1Statistics",
            "Atom1Z0Statistics",
            "Atom0DistanceStatistics",
            "Atom1DistanceStatistics",
            "Atom0DistanceXStatistics",
            "Atom1DistanceXStatistics",
            "Atom0DistanceYStatistics",
            "Atom1DistanceYStatistics",
            "Atom0DistanceZStatistics",
            "Atom1DistanceZStatistics",
            "TypeX0Statistics",
            "TypeX1Statistics",
            "TypeY0Statistics",
            "TypeY1Statistics",
            "TypeZ0Statistics",
            "TypeZ1Statistics",
            "TypeDistanceStatistics",
            "TypeDistanceXStatistics",
            "TypeDistanceYStatistics",
            "TypeDistanceZStatistics",
            # "FermiContact",
            # "SpinDipolar",
            # "ParaMagneticSpinOrbit",
            # "DiamagneticSpinOrbit",
        ]

        # target name
        # sub-target: "fc", "sd", "pso", "dso"
        # target: "scalar_coupling_constant"
        self.target_name = "fc"

        # whether save X
        self.save_X = True

        # whether excute tuning
        self.tuning = False

        # number of trials for tuning
        self.n_trials = 1

        # number of splits for data
        self.n_splits = 2

        # whether save the predicted values
        self.save = False

        # study name and storage path of parameters for the best model
        self.study_name = f"lgb_{self.target_name}"
        self.storage_path = f"../database/{self.study_name}.db"

        # static parameters for model
        self.fixed_params = {
            "boosting_type": "gbdt",
            "max_depth": 20,
            "learning_rate": 1e-1,
            "n_estimators": 100000,
            "reg_alpha": 0.0,
            # "metric": "binary",
        }

        # parameter space for searching with optuna
        self.param_space = {
            "num_leaves": IntParamSpace("num_leaves", 2, 100),
            "subsample": UniformParamSpace("subsample", 0.5, 1.0),
            "subsample_freq": IntParamSpace("subsample_freq", 1, 20),
            "colsample_bytree": LogUniformParamSpace("colsample_bytree", 1e-2, 1e-1),
            "min_child_weight": LogUniformParamSpace("min_child_weight", 1e-3, 1e1),
            "min_child_samples": IntParamSpace("min_child_samples", 1, 50),
            "reg_lambda": LogUniformParamSpace("reg_lambda", 1e-1, 1e4),
        }

        self.lr_params = {
            "penalty": "l2",
            "dual": False,
            "tol": 0.0001,
            "C": 1.0,
            "fit_intercept": True,
            "intercept_scaling": 1,
            "class_weight": None,
            "random_state": None,
            "solver": "warn",
            "max_iter": 100,
            "multi_class": "warn",
            "verbose": 0,
            "warm_start": False,
            "n_jobs": None,
            "l1_ratio": None,
        }

        # random seed
        self.seed = 42
