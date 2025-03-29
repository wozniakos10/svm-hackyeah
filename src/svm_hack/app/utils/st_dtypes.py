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
    YOUNG = '20-25 lat'
    MIDDLE_AGE = '26-35 lat'
    OLDER = '36-50 lat'


@unique
class HorizonttBox(StreamlitEnum):
    SHORT = 'krótkoterminowy'