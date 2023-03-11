__all__ = ["assert_never"]

import typing as T


def assert_never(arg: T.NoReturn) -> T.NoReturn:
    raise AssertionError("Expected code to be unreachable")
