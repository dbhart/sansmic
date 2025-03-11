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
        return f"{self.__code} ~> {self.__base}"

    @classmethod
    def _missing_(cls, value):
        return cls[value]
    

class small_len_unit(factor, ReprEnum):
    """For casing diameters, internal units are inches.
    
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
    inch = '[in_i]', 1, '[in_i]'
    foot = '[ft_i]', 12, '[in_i]'
    millimeter = 'mm', Fraction(10, 254), '[in_i]'
    centimeter = 'cm', Fraction(100, 254), '[in_i]'


class large_len_unit(factor, ReprEnum):
    """For depths and cavern radii, internal units are feet.
    
    Accepted codes for inputs are:
    ``[ft_i]``
        feet (international)
    ``[ft_us]``
        feet ("deprecated" U.S. survey)
    ``m``
        meters
    """
    foot = '[ft_i]', 1, '[ft_i]'
    survey_foot = '[ft_us]', Fraction(1_000_000, 999_998), '[ft_i]'
    meter = 'm', Fraction(10_000, 3_048), '[ft_i]'


class const_flow_unit(factor, ReprEnum):
    """Constant flowrate simulations are stored internally in bbl/d.
    
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
    barrels_per_day = '[bbl_us]/d', 1, '[bbl_us]/d'
    barrels_per_hour = '[bbl_us]/h', 24, '[bbl_us]/d'
    barrels_per_minute = '[bbl_us]/min', 1440, '[bbl_us]/d'
    cubic_meters_per_day = 'm3/d', Fraction(1_000_000_000_000, 158_987_294_928), '[bbl_us]/d'
    cubic_meters_per_hour = 'm3/h', Fraction(24_000_000_000_000, 158_987_294_928), '[bbl_us]/d'
    cubic_meters_per_minute = 'm3/min', Fraction(1_440_000_000_000_000, 158_987_294_928), '[bbl_us]/d'


class table_flow_unit(factor, ReprEnum):
    """Variable flowrate simulations are stored internally in bbl/h.
    
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
    barrels_per_day = '[bbl_us]/d', Fraction(1, 24), '[bbl_us]/h'
    barrels_per_hour = '[bbl_us]/h', 1, '[bbl_us]/h'
    barrels_per_minute = '[bbl_us]/min', 60, '[bbl_us]/h'
    cubic_meters_per_day = 'm3/d', Fraction(1_000_000_000_000, 3_815_695_078_272), '[bbl_us]/h'
    cubic_meters_per_hour = 'm3/h', Fraction(1_000_000_000_000, 158_987_294_928), '[bbl_us]/h'
    cubic_meters_per_minute = 'm3/min', Fraction(60_000_000_000_000, 158_987_294_928), '[bbl_us]/h'


class time_unit(factor, ReprEnum):
    """Internal time units are stored in fractional hours.
    
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
    second = 's', Fraction(1, 3_600), 'h'
    minute = 'min', Fraction(1, 60), 'h'
    hour = 'h', 1, 'h'
    day = 'd', 24, 'h'
    week = 'wk', 168, 'h'
    month_ave = 'mo_j', Fraction(1461, 2), 'h'
    year = 'a_j', 8766, 'h'


class density_unit(factor, ReprEnum):
    """Internal density units are generally in g/cm3 or in specific gravity (sg).
    Specific gravity is treated as if it were the density at 75 °F (23.889 °C).

    Accepted codes for density inputs:
    ``g/cm3``
        grams per cubic centimeter 
    ``kg/m3``
        kilograms per cubic meter
    ``t/m3``
        metric tons (tonnes) per cubic meter
    ``g/mL``, ``g/ml``
        grams per milliliter (millilitre)
    ``g/dL``, ``g/dl``
        grams per deciliter (decilitre)
    ``kg/L``, ``kg/l``
        kilograms per liter (litre)
    ``g%``
        gram-percent (``100 g% = 1 g/cm3``)
    ``{s.g.}``, ``{sg}``, ``{SG}``
        specific gravity
    ``[lb_av]/[in_i]3``
        pounds (avoirdupois) per cubic inch
    ``[lb_av]/[gal_us]``
        pounds per U.S. (liquid) gallon
    ``[lb_av]/[ft_i]3``
        pounds per cubic foot
    ``[lb_av]/[bbl_us]``
        pounds per (oil) barrel
    """
    gram_per_cm3 = 'g/cm3', 1, 'g/cm3'
    gram_per_milliliter = 'g/mL', 1, 'g/cm3'
    gram_per_millilitre = 'g/ml', 1, 'g/cm3'
    gram_per_deciliter = 'g/dL', Fraction(1,100), 'g/cm3'
    gram_per_decilitre = 'g/dl', Fraction(1,100), 'g/cm3'
    gram_percent = 'g%', Fraction(1, 100), 'g/cm3'
    kilogram_per_cubic_meter = 'kg/m3', Fraction(1,1000), 'g/cm3'
    kilogram_per_liter = 'kg/L', Fraction(1, 1000), 'g/cm3'
    kilogram_per_litre = 'kg/l', Fraction(1, 1000), 'g/cm3'
    metric_ton_per_cubic_meter =  't/m3', 1, 'g/cm3'
    tonne_per_cubic_meter = metric_ton_per_cubic_meter
    specific_gravity = r'{s.g.}', 1, 'g/cm3'
    sg = r'{sg}', 1, 'g/cm3'
    SG = r'{SG}', 1, 'g/cm3'
    pounds_per_cubic_inch = '[lb_av]/[in_i]', Fraction(453_592_370, 16_387_064), 'g/cm3'
    pounds_per_gallon = '[lb_av]/[gal_us]', Fraction(453_592_370, 3_785_411_784), 'g/cm3'
    pounds_per_cubic_foot = '[lb_av]/[ft_i]', Fraction(453_592_370, 28_316_846_592), 'g/cm3'
    pounds_per_barrel = '[lb_av]/[bbl_us]', Fraction(453_592_370, 158_987_294_928), 'g/cm3'


class to_si(factor, ReprEnum):
    """Unit conversion factors to base SI units (m, kg, s, K).
    
    Regarding the international foot and survey foot: the United States, as provided in Federal 
    Register (October 5, 2020, 85 FR 62698, p. 62698), has deprecated the U.S. Survey Foot and
    has indicated that it should be phased out for all but use with historical data in favor of
    the international foot (which has been the legal "foot" for all but land surveys and geodessy 
    in the U.S. since 1959). 
    
    Beginning January 1, 2023, the historical Gunter's, or chain-based, survey measures, i.e., the
    link, rod, chain, furlong, mile, section, acre and acre-foot, will continue to be defined 
    based on their relationship to "a foot" - i.e., an acre is still 43560 square feet and a
    furlong is still 660 feet. NIST has decided that, because historical survey measures
    are inherently less accurate than the difference between the international and survey foot -
    the survey foot is only 2 parts per million larger than the international foot - there is
    no need to make any changes to real property descriptions.

    For practical purposes, this means that real property of 1.25 acres is still 1.25 acres even
    though a conversion to meters will now result in a smaller value if all decimal points are 
    used. The difference between the sft and ift is truly significant only in geodessy and in map 
    coordinates where using the wrong foot could result in mis-loactions by tens of feet.

    The UCUM does not yet have a code (as of version 2.2) for the international acre. Thus, 
    sansmic uses the code ``43560.[sft_i]`` for an acre defined using the international foot
    rather than the more convenient ``[acr_us]``. Hopefully the acre based
    on the international foot will be added in the next release of the UCUM.

    Combined units, such as ``[bbl_us]/d`` are parsed and processed accordingly.
    """

    inch = '[in_i]', Fraction(254, 10_000), 'm'
    """The standard inch (1 in := 25.4 mm)"""
    foot = '[ft_i]', Fraction(3_048, 10_000), 'm'
    """The international foot; the US foot since 1959 (1 ft := 1 ift := 0.3048 m)"""
    yard = '[yd_i]', Fraction(9_144, 10_000), 'm'
    """The international yard; the US yard since 1959 (1 yd := 0.9144 m)"""
    mile = '[mi_i]', Fraction(16_093_440, 10_000), 'm'
    """The international mile; the US mile since 1959 (1 mi := 5280 ift)"""
    survey_foot = '[ft_us]', Fraction(1_200, 3_937), 'm'
    """The deprecated U.S. survey foot (1 sft := 1200/3937 m) (deprecated as of Jan 1, 2023; used from 1959-2022 for purposes of mapping coordinates and surveying only)"""
    square_inch = '[sin_i]', Fraction(64_516, 100_000_000), 'm2'
    """The square inch"""
    square_foot = '[sft_i]', Fraction(9_290_304, 100_000_000), 'm2'
    """The square foot"""
    acre = '43560.[sft_i]', Fraction(404_685_642_240, 100_000_000), 'm2'
    """The acre, defined as 43560 square feet; as of Jan 1, 2023, the acre is defined using the international foot"""
    survey_acre = '[acr_us]', Fraction(62_726_400_000, 15_499_969), 'm2'
    """The acre, defined as 43560 square feet; prior to Jan 1, 2023, the acre was defined using the US Survey Foot"""
    cubic_inch = '[cin_i]', Fraction(16_387_064, 1_000_000_000_000), 'm3'
    """The cubic inch"""
    cubic_foot = '[cft_i]', Fraction(28_316_846_592, 1_000_000_000_000), 'm3'
    """The (international) cubic foot"""
    gallon = '[gal_us]'
    """The US liquid gallon (1 gal := 1 liq gal := 1 gal (US) := 231 in^3)"""
    barrel = '[bbl_us]', Fraction(158_987_294_928, 1_000_000_000_000), 'm3'
    """The oil barrel (1 bbl := 42 liq gal (US))"""
    thousand_barrels = '10^3.[bbl_us]', Fraction(158_987_294_928, 1_000_000_000), 'm3'
    """One thousand barrels (1 Mbbl := 10^3 bbl) (note: this is **not** the prefix "mega-", it is "M = mille = thousand", a "customary" prefix)"""
    million_barrels = '10^6.[bbl_us]', Fraction(158_987_294_928, 1_000_000), 'm3'
    """One million barrels (1 MMbbl := 10^6 bbl) (note: this is **not** the prefix "mega-" - it is also not the Roman numeral "MM=2000" - it is "M" x "M" = 1000000)"""
    centimeter = 'cm', Fraction(1, 100), 'm'
    """Centimeter"""
    meter = 'm', 1, 'm'
    "Meter"
    square_centimeter = 'cm2', Fraction(1, 10_000), 'm2'
    "Square centimeter or centimetre squared"
    square_meter = 'm2', 1, 'm2'
    "Square meter or metre squared"
    hectare = 'ha', 10_000, 'm2'
    "Hectare (1 ha := 10000 m^2)"
    milliliter = 'mL', Fraction(1, 1_000_000), 'm3'
    "Milliliter or millilitre"
    liter = 'L', Fraction(1, 1_000), 'm3'
    "Liter or litre"
    cubic_centimeter = 'cm3', Fraction(1, 1_000_000), 'm3'
    """Cubic centimeter or centimetre cubed"""
    cubic_meter = 'm3', 1, 'm3'
    """Cubic meter or metre cubed"""
