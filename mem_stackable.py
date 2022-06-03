# This is a sub-class that is a "stackable" in-memory data store.
# A new one is used for each transaction.

from typing import Optional

from value_counter import ValueCounter

class ParentNotFoundException(Exception):
    pass


class MemStackable:
    def __init__(self, parent):
        # Parent is None when we are the root.
        self._parent = parent
        # Our primary dictionary for items we are storing.
        self._mem_dict = {}
        self._value_counter = ValueCounter()

    def set(self, name: str, value: str):
        self._decrement_value_if_needed(name)
        # Now that the counter has been dealt with, update the value and counter!
        self._value_counter.increment_value(value)
        self._mem_dict[name] = value

    def get(self, name: str) -> Optional[str]:
        if name in self._mem_dict:
            return self._mem_dict[name]
        if self._parent:
            return self._parent.get(name)
        return None

    def unset(self, name: str):
        self._decrement_value_if_needed(name)
        if self._parent is None:
            if name in self._mem_dict:
                del self._mem_dict[name]
        else:
            # If we are _not_ at the root, we need to store a None as an override
            self._mem_dict[name] = None

    def commit_to_parent(self):
        """Take all the changes that are part of this stackable transaction and apply them."""
        if self._parent is None:
            raise ParentNotFoundException
        for (name, value) in self._mem_dict.items():
            if value is None:
                self._parent.unset(name)
            else:
                self._parent.set(name, value)

    def num_equal_to(self, value: str) -> int:
        """Recursively go down the stack to determine how many have this value"""
        if self._parent is None:
            return self._value_counter.get_value_count(value)
        return self._value_counter.get_value_count(value) + self._parent.num_equal_to(value)

    def _decrement_value_if_needed(self, name: str):
        """Figure out if we are overriding 'name' at our layer and decrement it here if we are!"""
        if name in self._mem_dict:
            # We already know about this item at our layer in the stack,
            # so we must decrement *our* value counter for the old value.
            # (unless it's None; we don't track keys that don't exist)
            if self._mem_dict[name] is not None:
                self._value_counter.decrement_value(self._mem_dict[name])
        else:
            # This item isn't at our layer in the stack, but it might be
            # in a previous layer. If the name exists in a previous layer,
            # we need to decrement the value for it at our layer since we
            # are (temporarily, perhaps) removing its value.
            if self._parent:
                parent_value = self._parent.get(name)
                if parent_value is not None:
                    # We are overriding the key 'name' which previously held the value 'parent_value',
                    # so we have to decrement it at our layer.
                    self._value_counter.decrement_value(parent_value)
