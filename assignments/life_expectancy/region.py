"""Contains country enumerations."""
# coding: utf-8


from enum import Enum
import typing

__author__ = "Joaquim Leitão"
__email__ = "joaquim.leitao@nos.pt"


class Region(Enum):
    """
    Enum class containing all regions found in the raw life expectancy data
    """

    AL = "AL"
    AM = "AM"
    AT = "AT"
    AZ = "AZ"
    BE = "BE"
    BG = "BG"
    BY = "BY"
    CH = "CH"
    CY = "CY"
    CZ = "CZ"
    DE = "DE"
    DE_TOT = "DE_TOT"
    DK = "DK"
    EA18 = "EA18"
    EA19 = "EA19"
    EE = "EE"
    EEA30_2007 = "EEA30_2007"
    EEA31 = "EEA31"
    EFTA = "EFTA"
    EL = "EL"
    ES = "ES"
    EU27_2007 = "EU27_2007"
    EU27_2020 = "EU27_2020"
    EU28 = "EU28"
    FI = "FI"
    FR = "FR"
    FX = "FX"
    GE = "GE"
    HR = "HR"
    HU = "HU"
    IE = "IE"
    IS = "IS"
    IT = "IT"
    LI = "LI"
    LT = "LT"
    LU = "LU"
    LV = "LV"
    MD = "MD"
    ME = "ME"
    MK = "MK"
    MT = "MT"
    NL = "NL"
    NO = "NO"
    PL = "PL"
    PT = "PT"
    RO = "RO"
    RS = "RS"
    RU = "RU"
    SE = "SE"
    SI = "SI"
    SK = "SK"
    SM = "SM"
    TR = "TR"
    UA = "UA"
    UK = "UK"
    XK = "XK"

    @classmethod
    def list_all_countries(cls) -> typing.List[str]:
        """
        Lists all valid regions contained in the enum Region class, i.e., excludes countries such
        as EU28, EFTA, etc
        :return: List of string values, containing all the valid regions
        """
        invalid_countries = [
            cls.DE_TOT,
            cls.EEA30_2007,
            cls.EU27_2007,
            cls.EU27_2020,
            cls.EEA31,
            cls.EFTA,
            cls.EA18,
            cls.EA19,
            cls.EU28,
        ]
        return [region.value for region in cls if region not in invalid_countries]

    @classmethod
    def has_member_key(cls, item: str) -> bool:
        """
        Checks if a given item is present in the enum Region class (converts the value to upper
        case)
        :param item: The item intended to be checked for presence in the Region class
        :return: True if the item is present in the Region class, and False otherwise
        """
        return item.upper() in cls.__members__
