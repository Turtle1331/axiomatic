from __future__ import annotations


__all__ = ["Term", "Bottom", "Variable", "Implication", "Application"]

from dataclasses import dataclass

import typing as T


@dataclass(frozen=True)
class Bottom:
    pass


@dataclass(frozen=True)
class Variable:
    name: str


@dataclass(frozen=True)
class Implication:
    premise: Term
    conclusion: Term


@dataclass(frozen=True)
class Application:
    implication: Implication
    premise: Term


Term = Bottom | Variable | Implication | Application
