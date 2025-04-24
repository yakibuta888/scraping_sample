from dataclasses import dataclass
from abc import ABCMeta

@dataclass(frozen=True, eq=True)
class DataClassBase(metaclass=ABCMeta):
    """
    Base class for all data classes in the application.
    This class is frozen and uses equality comparison.
    """
    def __post_init__(self):
        # Ensure that all fields are frozen and immutable
        for field in self.__dataclass_fields__:
            if not self.__dataclass_fields__[field].init:
                raise ValueError(f"Field '{field}' must be initialized in the constructor.")
        # Additional post-initialization logic can be added here if needed