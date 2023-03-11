from __future__ import annotations


import typing as T

from propositions import Term, Variable
from shorthand import imply, apply


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


if __name__ == "__main__":
    main()
