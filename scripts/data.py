import os

from collections import namedtuple

from .config import Config
from .db import LocalFile
from .utility import reduce_mem_usage
from .preprocess import Preprocessor


class DatasetCreator:
    def __init__(self):
        self.config = Config()

    def run(self):
        # load files
        db = LocalFile(self.config)
        train = db.get_train()
        test = db.get_test()
        # dipole_moments = db.get_dipole_moments()
        # magnetic_shielding_tensors = db.get_magnetic_shielding_tensors()
        # mulliken_charges = db.get_mulliken_charges()
        # potential_energy = db.get_potential_energy()
        scalar_coupling_contributions = db.get_scalar_coupling_contributions()
        structures = db.get_structures()

        if not os.path.isfile(self.config.pickled_train_path):
            # reduce memory usage
            train = reduce_mem_usage(train, "train")
            test = reduce_mem_usage(test, "test")
            # dipole_moments = reduce_mem_usage(dipole_moments, "dipole_moment")
            # magnetic_shielding_tensors = reduce_mem_usage(magnetic_shielding_tensors, "magnetic_shielding_tensors")
            # mulliken_charges = reduce_mem_usage(mulliken_charges, "mulliken_charges")
            # potential_energy = reduce_mem_usage(potential_energy, "potential_energy")
            scalar_coupling_contributions = reduce_mem_usage(
                scalar_coupling_contributions, "scalar_coupling_contributions"
            )
            structures = reduce_mem_usage(structures, "structures")

            # preprocess data
            preprocessor = Preprocessor()
            train, test, structures = preprocessor.run(
                train, test, structures, scalar_coupling_contributions
            )

            # save preprocessed dataframe to pickle
            train.to_pickle(self.config.pickled_train_path)
            test.to_pickle(self.config.pickled_test_path)
            structures.to_pickle(self.config.pickled_structures_path)

        # create dataset
        Dataset = namedtuple(
            "Dataset",
            [
                "train",
                "test",
                # "dipole_moments",
                # "magnetic_shielding_tensors",
                # "mulliken_charges",
                # "potential_energy",
                "structures",
            ],
        )
        dataset = Dataset(
            train,
            test,
            # dipole_moments.set_index("molecule_name"),
            # magnetic_shielding_tensors.set_index("molecule_name"),
            # mulliken_charges.set_index("molecule_name"),
            # potential_energy.set_index("molecule_name"),
            structures.set_index("molecule_name"),
        )
        return dataset
