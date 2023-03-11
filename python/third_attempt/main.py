from __future__ import annotations


import dataclasses as D
import json

import typing as T

from propositions import Term, Variable, Implication, Application
from shorthand import imply, apply
from unifier import unify, verify, decompose, substitute


X = Variable("X")
Y = Variable("Y")
Z = Variable("Z")

I: Term = imply(X, X)
K: Term = imply(X, (Y, X))
S: Term = imply((X, Y, Z), (X, Y), X, Z)


def main():
    skk = apply(S, K, K)
    print(skk)

    # unify SKK
    P = Variable("P")
    Q = Variable("Q")
    modus_ponens = apply(imply(P, Q), P)

    unify({(skk, modus_ponens)})


if __name__ == "__main__":
    main()
