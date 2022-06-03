
from mem_stackable import MemStackable

class NoTransactionException(Exception):
    """We tried to commit or rollback outside of a transaction. Oops."""
    pass


class MemRed:
    def __init__(self):
        self._transactional_stack = [MemStackable(None)]

    def set(self, name: str, value: str):
        self._transactional_stack[-1].set(name, value)

    def get(self, name: str) -> str:
        return self._transactional_stack[-1].get(name)

    def unset(self, name: str):
        self._transactional_stack[-1].unset(name)

    def num_equal_to(self, value: str) -> int:
        return self._transactional_stack[-1].num_equal_to(value)

    def begin(self):
        new_stackable = MemStackable(self._transactional_stack[-1])
        self._transactional_stack.append(new_stackable)

    def commit(self):
        if len(self._transactional_stack) == 1:
            raise NoTransactionException
        for i in range(len(self._transactional_stack) - 1):
            self._transactional_stack[-(i+1)].commit_to_parent()
        del self._transactional_stack[1:]

    def rollback(self):
        if len(self._transactional_stack) == 1:
            raise NoTransactionException
        # Rolling back is very simple!
        del self._transactional_stack[-1]