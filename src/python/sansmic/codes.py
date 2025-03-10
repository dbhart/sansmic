# coding: utf-8

"""
Provide lists of acceptable shortcut codes for I/O and configuration files.
"""

from collections import namedtuple
from dataclasses import dataclass
from enum import ReprEnum
from fractions import Fraction

class factor(float):
    def __new__(cls, code, factor, base):
        self = float.__new__(cls, factor)
        self.__init__(code, factor, base)
        self._value_ = self
        return self

    def __init__(self, code, factor, base):
        self.__code = code
        self.__base = base
        self.__factor = factor
        self.__class__._member_map_[code] = self

    @property
    def code(self):
        return self.__code

    @property
    def base(self):
        return self.__base

    @property
    def factor(self):
        return self.__factor

    def __str__(self):
        return self.__code

    def __repr__(self):
        return f"{self.__code} ~ {self.__base}"

    @classmethod
    def _missing_(cls, value):
        return cls[value]
    

class small_len_unit(factor, ReprEnum):
    """For casing diameters, internal units are inches."""
    inch = '[in_i]', 1, '[in_i]'
    foot = '[ft_i]', 12, '[in_i]'
    millimeter = 'mm', Fraction(10, 254), '[in_i]'
    centimeter = 'cm', Fraction(100, 254), '[in_i]'


class large_len_unit(factor, ReprEnum):
    """For depths and cavern radii, internal units are feet."""
    foot = '[ft_i]', 1, '[ft_i]'
    survey_foot = '[ft_us]', Fraction(1_000_000, 999_998), '[ft_i]'
    meter = 'm', Fraction(10_000, 3_048), '[ft_i]'


class const_flow_unit(factor, ReprEnum):
    """Constant flowrate simulations are internally in bbl/."""
    barrels_per_day = '[bbl_us]/d', 1, '[bbl_us]/d'
    barrels_per_hour = '[bbl_us]/h', 24, '[bbl_us]/d'
    barrels_per_minute = '[bbl_us]/min', 1440, '[bbl_us]/d'
    cubic_meters_per_day = 'm3/d', Fraction(1_000_000_000_000, 158_987_294_928), '[bbl_us]/d'
    cubic_meters_per_hour = 'm3/h', Fraction(24_000_000_000_000, 158_987_294_928), '[bbl_us]/d'
    cubic_meters_per_minute = 'm3/min', Fraction(1_440_000_000_000_000, 158_987_294_928), '[bbl_us]/d'


class table_flow_unit(factor, ReprEnum):
    """Variable flowrate simulations are internally in bbl/h"""
    barrels_per_day = '[bbl_us]/d', Fraction(1, 24), '[bbl_us]/h'
    barrels_per_hour = '[bbl_us]/h', 1, '[bbl_us]/h'
    barrels_per_minute = '[bbl_us]/min', 60, '[bbl_us]/h'
    cubic_meters_per_day = 'm3/d', Fraction(1_000_000_000_000, 3_815_695_078_272), '[bbl_us]/h'
    cubic_meters_per_hour = 'm3/h', Fraction(1_000_000_000_000, 158_987_294_928), '[bbl_us]/h'
    cubic_meters_per_minute = 'm3/min', Fraction(60_000_000_000_000, 158_987_294_928), '[bbl_us]/h'


class duration_unit(factor, ReprEnum):
    """Internal durations are in hours"""
    second = 's', Fraction(1, 3_600), 'h'
    minute = 'min', Fraction(1, 60), 'h'
    hour = 'h', 1, 'h'
    day = 'd', 24, 'h'
    week = 'wk', 168, 'h'
    month_ave = 'mo_j', Fraction(1461, 2), 'h'
    year = 'a_j', 8766, 'h'


class to_si(factor, ReprEnum):
    """Unit conversion factors back to base SI units"""

    inch = '[in_i]', Fraction(254, 10_000), 'm'
    foot = '[ft_i]', Fraction(3_048, 10_000), 'm'
    yard = '[yd_i]', Fraction(9_144, 10_000), 'm'
    mile = '[mi_i]', Fraction(16_093_440, 10_000), 'm'
    survey_foot = '[ft_us]', Fraction(1_200, 3_937), 'm'
    square_inch = '[sin_i]', Fraction(64_516, 100_000_000), 'm2'
    square_foot = '[sft_i]', Fraction(9_290_304, 100_000_000), 'm2'
    acre = '43560.[ft_i]2', Fraction(404_685_642_240, 100_000_000), 'm2'
    survey_acre = '[acr_us]', Fraction(62_726_400_000, 15_499_969), 'm2'
    cubic_inch = '[cin_i]', Fraction(16_387_064, 1_000_000_000_000), 'm3'
    cubic_foot = '[cft_i]', Fraction(28_316_846_592, 1_000_000_000_000), 'm3'
    barrel = '[bbl_us]', Fraction(158_987_294_928, 1_000_000_000_000), 'm3'
    thousand_barrels = '10^3.[bbl_us]', Fraction(158_987_294_928, 1_000_000_000), 'm3'
    million_barrels = '10^6.[bbl_us]', Fraction(158_987_294_928, 1_000_000), 'm3'
    centimeter = 'cm', Fraction(1, 100), 'm'
    meter = 'm', 1, 'm'
    square_centimeter = 'cm2', Fraction(1, 10_000), 'm2'
    square_meter = 'm2', 1, 'm2'
    hectare = 'ha', 10_000, 'm2'
    milliliter = 'mL', Fraction(1, 1_000_000), 'm3'
    liter = 'L', Fraction(1, 1_000), 'm3'
    cubic_centimeter = 'cm3', Fraction(1, 1_000_000), 'm3'
    cubic_meter = 'm3', 1, 'm3'
    barrels_per_day = '[bbl_us]/d', Fraction(158_987_294_928, 1_000_000_000_000), 'm3/d'
    barrels_per_hour = '[bbl_us]/h', Fraction(158_987_294_928, 1_000_000_000_000), 'm3/h'
