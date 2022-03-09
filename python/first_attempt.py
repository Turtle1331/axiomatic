import typing as T
from dataclasses import dataclass
from functools import lru_cache


'''Propositions (types)'''

class UConst(T.NamedTuple):
    name: T.AnyStr
    
    def __str__(self):
        return self.name

class UAxiom(T.NamedTuple)

class UImplies(T.NamedTuple):
    from_: 'UAny'
    to: 'UAny'
    
    def __str__(self):
        return f'({self.from_} -> {self.to})'

UAny = T.Union[UConst, UImplies]

def uChained(head, *tail):
    if not tail:
        return head
    return UImplies(
        head,
        uChained(tail[0], *tail[1:])
    )

def uK(a, b):
    return uChained(a, b, a)

def uS(a, b):
    return uChained(
        uChained(a, b, c),
        uChained(a, b),
        a,
        c
    )


'''Proofs (type inhabitations)'''

class IAxiom(T.NamedTuple):
    scheme: 'UConst'
    
    
    def __str__(self):
        return f'IAxiom({self.type})'

class IApply(T.NamedTuple):
    first: 'IExpr'
    second: 'IExpr'

def iK(a, b):
    return IAxiom(uK(a, b))

def iS(a, b, c):
    return IAxiom(uS(a, b, c))

IExpr = T.Union[IAxiom, IApply]


'''Deductive system (inhabitation rules)'''

class DLogicZero():
    pass

class DAxiomScheme():
    pass



def typecheck(expr):
    if isinstance(expr, IAxiom):
        return expr
    elif isinstance(expr, IApply):
        pass



P = UConst('P')
umain = uChained(P, P, P)


imain = iK(P, P)


print(imain)
