from enum import Enum, auto


class ValidationStatus(Enum):
    """
    Enum representing the status of a validation operation.

    Attributes:
        SUCCESS: Indicates that the validation was successful.
        WARNING: Indicates that there is a warning in the validation.
        FAILURE: Indicates that the validation failed.
    """
    SUCCESS = auto()
    WARNING = auto()
    FAILURE = auto()
