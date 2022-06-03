from collections import defaultdict


class ValueCounter:
    def __init__(self):
        self._value_dict = defaultdict(int)

    def get_value_count(self, value: str) -> int:
        """Return the count of 'value' in our system"""
        return self._value_dict.get(value, 0)

    def increment_value(self, value: str):
        """Increment our count of 'value' by one"""
        new_count = self._value_dict[value] + 1
        if new_count == 0:
            del self._value_dict[value]
        else:
            self._value_dict[value] = new_count

    def decrement_value(self, value: str):
        new_count = self._value_dict[value] - 1
        if new_count == 0:
            del self._value_dict[value]
        else:
            self._value_dict[value] = new_count
