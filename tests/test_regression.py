# coding: utf-8

import os
import unittest
from os.path import abspath, dirname, join

import numpy as np
import pandas as pd
import sansmic

testdir = dirname(abspath(str(__file__)))


class TestRegression(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.nameF = "baseline"
        self.datF = join(testdir, self.nameF + ".dat")
        self.tstF = sansmic.io.read_tst(join(testdir, self.nameF))
        self.resF = sansmic.io.read_classic_out_ddl(join(testdir, self.nameF))
        self.namePy = "regression"

    def runTest(self):
        model = sansmic.read_scenario(self.datF)
        sansmic.write_scenario(model, join(testdir, self.namePy + ".toml"))
        with model.new_simulation(join(testdir, self.namePy)) as sim:
            sim.run_sim()
        resPy = sim.results
        tstPy = sansmic.io.read_tst(join(testdir, self.namePy))
        Stats = sansmic.model.pd.DataFrame.from_dict(
            dict(
                rmse=np.sqrt(np.mean((self.tstF - tstPy) ** 2, 0)),
                max_rel=((self.tstF - tstPy).abs() / abs(self.tstF)).max(),
                rmse_rel_err=(np.sqrt(np.mean((self.tstF - tstPy) ** 2, 0)))
                / self.tstF.abs().max(),
                min_F=abs(self.tstF).min(),
                min_Py=abs(tstPy).min(),
                max_F=abs(self.tstF).max(),
                max_Py=abs(tstPy).max(),
            )
        )
        self.assertLessEqual(Stats.rmse_rel_err["t_d"], 1.0e-4)
        self.assertLessEqual(Stats.rmse_rel_err["V_cav"], 5.0e-4)
        self.assertLessEqual(Stats.rmse_rel_err["err_ode"], 5.0e-4)
        self.assertLessEqual(Stats.rmse_rel_err["sg_out"], 5.0e-4)
        self.assertLessEqual(Stats.rmse_rel_err["sg_ave"], 5.0e-4)
        self.assertLessEqual(Stats.rmse_rel_err["V_insol"], 1.0e-3)
        self.assertLessEqual(Stats.rmse_rel_err["z_insol"], 5.0e-4)
        self.assertLessEqual(Stats.rmse_rel_err["z_obi"], 5.0e-4)
        self.assertLessEqual(Stats.rmse_rel_err["V_vented"], 1.0e-2)
        self.assertLessEqual(Stats.rmse_rel_err["Q_inj"], 5.0e-4)
        self.assertLessEqual(Stats.rmse_rel_err["Q_fill"], 5.0e-4)
        self.assertLessEqual(Stats.rmse_rel_err["V_inj"], 1.0e-3)
        self.assertLessEqual(Stats.rmse_rel_err["V_fill"], 1.0e-3)