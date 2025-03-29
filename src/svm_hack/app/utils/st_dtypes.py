from enum import Enum, unique
from typing import List, Tuple


class StreamlitEnum(Enum):
    """Helper class to safety keep values from Streamlit selectboxes in Enum format"""
    def __str__(self) -> str:
        return self.value

    @classmethod
    def values(cls) -> list:
        return [s.value for s in cls]


@unique
class AgeBox(StreamlitEnum):
    YOUNG = '18-24 lata'
    MIDDLE_AGE = '25-34 lata'
    OLDER = '35-50 lat'
    SENIOR = 'powyżej 50 lat'


@unique
class HorizonttBox(StreamlitEnum):
    SHORT = 'krótkoterminowy (do 2 lat)'
    MEDIUM = 'średnioterminowy (do 5 lat)'
    LONG = 'długoterminowy (do 20 lat)'