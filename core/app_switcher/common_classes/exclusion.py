from enum import StrEnum, auto
class ExclusionType(StrEnum):
    EXE = auto()
    EXECUTABLE = auto()
    BUNDLE = auto()
    PATH = auto()
    NAME = auto()

class RunningApplicationExclusion:
    exclusion_type: ExclusionType 
    data_string: str

    def __init__(self, 
                 exclusion_type:ExclusionType, 
                 data_string: str):
        self.exclusion_type = exclusion_type
        self.data_string = data_string.lower()

    def __str__(self) -> str:
        return f"{self.exclusion_type} = {self.data_string}"