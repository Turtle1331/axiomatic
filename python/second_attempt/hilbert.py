__all__ = ('axiom_k', 'axiom_s', 'infer_mp')


from functional import *

from basics import *
from propositional import *


@compose(axiom)
def axiom_k(a, b):
    return chain(a, b, a)

@compose(axiom)
def axiom_s(a, b, c):
    return chain(chain(a, b, c), to(a, b), a, c)

@compose(inference, True)
def infer_mp(a, b):
    return (to(a, b), a), b

