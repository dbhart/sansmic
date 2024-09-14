# coding: utf-8

import os
import unittest
from os.path import abspath, dirname, join

import numpy as np
import pandas as pd
import sansmic.empirical as emp
import tempfile


class TestEmpirical(unittest.TestCase):
    """Verify that constants are correct. This is mostly for coverage
    purposes to validate that the constants are in the right place and to force changes to be documented by being in both the
    source code and in the tests.
    """

    def test_NaCl_solid_density(self):
        self.assertEqual(emp.rho_NaCl_s, 2.16)

    def test_recession_rate(self):
        self.assertEqual(len(emp.a), 6)

    def test_wt_pct_func(self):
        self.assertEqual(len(emp.c), 3)

    def test_sg_matrix(self):
        self.assertTupleEqual(emp.sg_matrix.shape, (15, 10))
        self.assertGreaterEqual(emp.sg_matrix.min(), 0.958)
        self.assertLessEqual(emp.sg_matrix.max(), 1.208)

    def test_wt_pct_vec(self):
        self.assertTupleEqual(emp.wt_pct_vec.shape, (15, 1))
        self.assertGreaterEqual(emp.wt_pct_vec.min(), 0.0)
        self.assertLessEqual(emp.wt_pct_vec.max(), 26.0)

    def test_T_degC_vec(self):
        self.assertTupleEqual(emp.T_degC_vec.shape, (1, 10))
        self.assertGreaterEqual(emp.T_degC_vec.min(), 0.0)
        self.assertLessEqual(emp.T_degC_vec.max(), 100.0)

    def test_wt_pct_max(self):
        self.assertTupleEqual(emp.wt_pct_max.shape, (10,))

    def test_T_degC_max(self):
        self.assertTupleEqual(emp.T_degC_max.shape, (10,))

    def test_sg_max(self):
        self.assertTupleEqual(emp.sg_max.shape, (10,))
