from collections import defaultdict

class AttemptedDecrementZeroValue(Exception):
    """We should not be attempting to decrement a value that is not stored."""
    pass

class ValueCounter:
    def __init__(self):
        self._value_dict = defaultdict(int)

    def get_value_count(self, value: str) -> int:
        """Return the count of 'value' in our system"""
        return self._value_dict.get(value, 0)

    def increment_value(self, value: str):
        """Increment our count of 'value' by one"""
        self._value_dict[value] += 1

    def decrement_value(self, value: str):
        if value in self._value_dict:
            old_count = self._value_dict[value]
            if old_count > 1:
                self._value_dict[value] = old_count - 1
            else:
                # Don't clutter the system with empty values
                del self._value_dict[value]
        else:
            raise AttemptedDecrementZeroValue(value)
