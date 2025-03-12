# coding: utf-8

"""
Provides enums of the accepted unit codes for input variables and output formats.

Recognized codes come from the `Uniform Codes for Units of Measurement` ([UCUM]_)
or the UNECE Rec 20 `Codes for Units Of Measure Used in International Trade` (:term:`UNECE`) 
coding systems. UCUM codes must be the **case-sensitive** code; UNECE codes should
be provided in uppercase.
"""

from collections import namedtuple
from dataclasses import dataclass
from enum import ReprEnum, nonmember
from fractions import Fraction

class Unit(float):
    """
    Base type for unit enum members, provides the code as string and the
    conversion factor to the sansmic internal unit as a float, int or fraction.
    """

    def __new__(cls, code, factor):
        self = float.__new__(cls, factor)
        self.__init__(code, factor)
        self._value_ = self
        return self

    def __init__(self, code, factor):
        self.__code = code
        self.__factor = factor
        self.__class__._member_map_[code] = self

    @property
    def code(self):
        """The unit code that is recognized"""
        return self.__code

    @property
    def factor(self):
        """The conversion factor to the internal units"""
        return self.__factor

    def __str__(self):
        return self.__code

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.__code)})"

    @classmethod
    def _missing_(cls, value):
        return cls[value]
    

class SmallLengthsUnit(Unit, ReprEnum):
    """Convert casing radii to inches, the internal unit.
    Recognized codes come from either :term:`UCUM` (in ``TT`` font) or :term:`UNECE` 
    (in `it` font) coding systems. Codes are **case sensitive**.

    Accepted codes for inputs are:
    ``[in_i]`` 
        inches
    ``[ft_i]``
        feet (international)
    ``mm``
        millimeters
    ``cm``
        centimeters
    """
    @property
    def internal_unit(self):
        """The code for the internally-used units"""
        return '[in_i]'

    ucum_international_inch = '[in_i]', 1
    ucum_international_foot = '[ft_i]', 12
    ucum_millimeter = 'mm', Fraction(10, 254)
    ucum_centimeter = 'cm', Fraction(100, 254)
    unece_inch = 'INH', 1
    unece_foot = 'FOT', 12
    unece_millimeter = 'MMT', Fraction(10, 254)
    unece_centimeter = 'CMT', Fraction(100, 254)


class LargeLengthsUnit(Unit, ReprEnum):
    """Convert depths and cavern radii to international feet, the internal unit.
    Recognized codes come from either :term:`UCUM` (in ``TT`` font) or :term:`UNECE` 
    (in `it` font) coding systems. Codes are **case sensitive**.
    
    Accepted codes for inputs are:
    ``[ft_i]`` or `FOT`
        foot (international)
    ``[ft_us]`` or `M51`
        foot ("deprecated" U.S. survey)
    ``m`` or `MTR`
        meters
    """
    @property
    def internal_unit(self):
        """The code for the internally-used units"""
        return '[ft_i]'

    ucum_international_foot = '[ft_i]', 1
    ucum_survey_foot = '[ft_us]', Fraction(1_000_000, 999_998)
    ucum_meter = 'm', Fraction(10_000, 3_048)
    unece_foot = 'FOT', 1
    unece_foot_us_survey = 'M51', Fraction(1_000_000, 999_998)
    unece_metre = 'MTR', Fraction(10_000, 3_048)


class VolumeUnit(Unit, ReprEnum):
    """
    Recognized codes come from either :term:`UCUM` (in ``TT`` font) or :term:`UNECE` 
    (in `it` font) coding systems. Codes are **case sensitive**.
    """
    @property
    def internal_unit(self):
        """The code for the internally-used units"""
        return '[bbl_us]'

    ucum_barrel = '[bbl_us]'
    ucum_cubic_foot = 'ft3', 1
    ucum_cubic_meter = 'm3'
    unece_cubic_metre = 'MTQ'
    unece_cubic_foot = 'FTQ', 1
    unece_barrel_us_petroleum = 'BLL'


class TimingUnit(Unit, ReprEnum):
    """Convert time units to hours, the internal unit.
    Recognized codes come from either :term:`UCUM` (in ``TT`` font) or :term:`UNECE` 
    (in `it` font) coding systems. Codes are **case sensitive**.

    The following codes can be used for solver step sizes, but not durations:
    ``s``
        seconds (useful for timesteps but not durations)
    ``min``
        minutes (useful for timesteps but not durations)


    Accepted codes for both solver step size and stage durations; also available as output formats:
    ``h``
        hours; display format: ``X.xx h``
    ``d``
        days (durations rounded to nearest timestep); display format: ``X d  Y.yy h``
    

    The following codes can be used for durations, but not solver step size, and are also availabe as output formats:
    ``wk``
        weeks (1 wk == 7 d); display format: ``X wk  Y.yy d``
    ``mo_j``
        months, Julian (1 mo_j == 30 d 10 h 30 min); display format: ``X mo  Y.yy d``
    ``a_j``
        years, Julian (1 a_j == 365 d 6 h); display format: ``X a_j  Y.yy d``


    Additional output formats for times are also available, see the input file help for details.
    """
    @property
    def internal_unit(self):
        """The code for the internally-used units"""
        return 'h'

    second = 's', Fraction(1, 3_600)
    minute = 'min', Fraction(1, 60)
    hour = 'h', 1
    day = 'd', 24
    week = 'wk', 168
    month_ave = 'mo_j', Fraction(1461, 2)
    year = 'a_j', 8766


class ConstantFlowrateUnit(Unit, ReprEnum):
    """Convert flow units for constant rates to barrels per day, the internal units.
    Recognized codes come from either :term:`UCUM` (in ``TT`` font) or :term:`UNECE` 
    (in `it` font) coding systems. Codes are **case sensitive**.

    Accepted codes for inputs are:
    ``[bbl_us]/d``
        barrels per day
    ``[bbl_us]/h``
        barrels per hour
    ``[bbl_us]/min``
        barrels per minute
    ``m3/d``
        cubic meters per day
    ``m3/h``
        cubic meters per hour
    ``m3/min``
        cubic meters per minute
    """
    @property
    def internal_unit(self):
        """The code for the internally-used units"""
        return '[bbl_us]/d'

    ucum_barrels_per_day = '[bbl_us]/d', 1
    ucum_barrels_per_hour = '[bbl_us]/h', 24
    ucum_barrels_per_minute = '[bbl_us]/min', 1440
    ucum_cubic_meters_per_day = 'm3/d', Fraction(1_000_000_000_000, 158_987_294_928)
    ucum_cubic_meters_per_hour = 'm3/h', Fraction(24_000_000_000_000, 158_987_294_928)
    ucum_cubic_meters_per_minute = 'm3/min', Fraction(1_440_000_000_000_000, 158_987_294_928)
    unece_barrel_us_petroleum_per_day = 'B1', 1
    unece_barrel_us_petroleum_per_hour = 'J62', 24
    unece_barrel_us_petroleum_per_minute = '5A', 1440
    unece_cubic_metre_per_day = 'G52'
    unece_cubic_metre_per_hour = 'MQH'
    unece_cubic_metre_per_minute = 'G53'


class VariableFlowrateUnit(Unit, ReprEnum):
    """Convert flow units for variable rates to barrels per hour, the internal units.
    Recognized codes come from either :term:`UCUM` (in ``TT`` font) or :term:`UNECE` 
    (in `it` font) coding systems. Codes are **case sensitive**.

    Accepted codes for inputs are:
    ``[bbl_us]/d``
        barrels per day
    ``[bbl_us]/h``
        barrels per hour
    ``[bbl_us]/min``
        barrels per minute
    ``m3/d``
        cubic meters per day
    ``m3/h``
        cubic meters per hour
    ``m3/min``
        cubic meters per minute
    """
    @property
    def internal_unit(self):
        """The code for the internally-used units"""
        return '[bbl_us]/h'

    ucum_barrels_per_day = '[bbl_us]/d', Fraction(1, 24)
    ucum_barrels_per_hour = '[bbl_us]/h', 1
    ucum_barrels_per_minute = '[bbl_us]/min', 60
    ucum_cubic_meters_per_day = 'm3/d', Fraction(1_000_000_000_000, 3_815_695_078_272)
    ucum_cubic_meters_per_hour = 'm3/h', Fraction(1_000_000_000_000, 158_987_294_928)
    ucum_cubic_meters_per_minute = 'm3/min', Fraction(60_000_000_000_000, 158_987_294_928)
    unece_barrel_us_petroleum_per_day = 'B1'
    unece_barrel_us_petroleum_per_hour = 'J62'
    unece_barrel_us_petroleum_per_minute = '5A'
    unece_cubic_metre_per_day = 'G52'
    unece_cubic_metre_per_hour = 'MQH'
    unece_cubic_metre_per_minute = 'G53'


class DensityUnits(Unit, ReprEnum):
    """Convert density units to specific gravity or grams per cubic centimeter.
    Recognized codes come from either :term:`UCUM` (in ``TT`` font) or :term:`UNECE` 
    (in `it` font) coding systems. Codes are **case sensitive**.

    Because temperature effects are currently off within the sansmic
    dissolution model, specific gravity inputs should be equal to the density
    of the fluid in g/mL at 75 °F (23.889 °C).

    Accepted codes for density inputs:
    ``g/cm3``
        grams per cubic centimeter 
    ``kg/m3``
        kilograms per cubic meter
    ``t/m3``
        metric tons (tonnes) per cubic meter
    ``g/mL``, ``g/ml``
        grams per milliliter (millilitre)
    ``kg/L``, ``kg/l``
        kilograms per liter (litre)
    ``{s.g.}``, ``{sg}``
        specific gravity
    ``[lb_av]/[ft_i]3``
        pounds per cubic foot; this can be used for inputs, only
    """
    @property
    def internal_unit(self):
        """The code for the internally-used units"""
        return r'{s.g.}'

    ucum_gram_per_cm3 = 'g/cm3', 1
    ucum_gram_per_milliliter = 'g/mL', 1
    ucum_gram_per_millilitre = 'g/ml', 1
    ucum_kilogram_per_cubic_meter = 'kg/m3', Fraction(1,1000)
    ucum_kilogram_per_liter = 'kg/L', Fraction(1, 1000)
    ucum_kilogram_per_litre = 'kg/l', Fraction(1, 1000)
    ucum_metric_ton_per_cubic_meter =  't/m3', 1
    specific_gravity = r'{s.g.}', 1
    sg = r'{sg}', 1
    ucum_pounds_per_cubic_foot = '[lb_av]/[cft_i]', Fraction(453_592_370, 28_316_846_592)
    ucum_pounds_per_foot_cubed = '[lb_av]/[ft_i]3', Fraction(453_592_370, 28_316_846_592)
    unece_pound_per_cubic_foot = '87', Fraction(453_592_370, 28_316_846_592)
