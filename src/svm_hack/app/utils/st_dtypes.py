from enum import Enum, unique


class StreamlitEnum(Enum):
    """Helper class to safety keep values from Streamlit selectboxes in Enum format"""

    def __str__(self) -> str:
        return self.value

    @classmethod
    def values(cls) -> list:
        return [s for s in cls]


@unique
class AgeBox(StreamlitEnum):
    YOUNG = "18-24 lata"
    MIDDLE_AGE = "25-34 lata"
    OLDER = "35-50 lat"
    SENIOR = "powyżej 50 lat"


@unique
class TimeHorizonBox(StreamlitEnum):
    SHORT = "krótkoterminowy (do 5 lat)"
    MEDIUM = "średnioterminowy (do 10 lat)"
    LONG = "długoterminowy (do 20 lat)"


@unique
class PercentMoneyBox(StreamlitEnum):
    LOW = "<10%"
    MED = "10-30%"
    HIGH = ">30%"


@unique
class ReactionBox(StreamlitEnum):
    LOW = "Sprzedałbym wszystko, żeby uniknąć dalszych strat"
    MED = "Poczekałbym, ale z niepokojem"
    HIGH = "Dokupiłbym więcej, widząc okazję"
