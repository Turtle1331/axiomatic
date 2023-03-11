from __future__ import annotations

__all__ = ["apply", "imply"]


from dataclasses import dataclass

import typing as T

from propositions import Term, Bottom, Implication, Application
from polyfill import assert_never


TermTree = Term | tuple["TermTree", ...]


def tree_reduce(op: T.Callable[[tuple[Term, ...]], Term]):
    def _reduce(tree: TermTree) -> Term:
        if isinstance(tree, Term):
            return tree

        if isinstance(tree, tuple):
            return op(tuple(map(_reduce, tree)))

        return assert_never(tree)

    def reduce(*tree: TermTree) -> Term:
        return _reduce(tree)

    return reduce


def _imply(terms: tuple[Term, ...]) -> Term:
    match len(terms):
        case 0:
            return Bottom()
        case 1:
            return terms[0]
        case _:
            return Implication(terms[0], _imply(terms[1:]))


def _apply(terms: tuple[Term, ...]) -> Term:
    match len(terms):
        case 0:
            return Bottom()
        case 1:
            return terms[0]
        case _:
            return Application(_apply(terms[-1:]), terms[-1])


imply = tree_reduce(_imply)
apply = tree_reduce(_apply)
