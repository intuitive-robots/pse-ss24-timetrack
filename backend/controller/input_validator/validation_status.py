from enum import Enum, auto


class ValidationStatus(Enum):
    """
    Enum representing the status of a validation operation.

    This Enum defines the possible outcomes of a validation check, helping to standardize the response
    across different validation operations within the application.

    :cvar SUCCESS: Indicates that the validation was successful.
    :cvar WARNING: Indicates that there is a warning in the validation.
    :cvar FAILURE: Indicates that the validation failed.
    """
    SUCCESS = auto()
    WARNING = auto()
    FAILURE = auto()
