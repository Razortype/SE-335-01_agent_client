from enum import Enum
from typing import Type

def from_string(cls):
    """
    Decorator to add a from_string method to an Enum class.
    Raises TypeError if not used with an Enum class.
    """
    if not issubclass(cls, Enum):
        raise TypeError("add_from_string decorator can only be applied to Enum classes.")

    @classmethod
    def from_string(cls: Type[Enum], value, raise_error=True):
        """
        Converts a string value (lowercase) to the corresponding enum member.
        Raises ValueError if no matching member found (if raise_error is True).
        Returns None if no matching member found (if raise_error is False).
        """
        if value:
            value = value.lower()
            for member in cls:
                if member.value == value:
                    return member
        if raise_error:
            raise ValueError(f"No enum member with value '{value}'")
        return None

    # Apply the decorator to the class method
    cls.from_string = classmethod(from_string)
    return cls