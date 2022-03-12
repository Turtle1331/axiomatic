from basics import *
from propositional import *
from hilbert import *

from functional import *
from verifier import *
from smart import *


try:
    import console
    console.clear()
except ImportError:
    pass



# allow K and S axioms and modus ponens inference rule
hilbert_ks = deductive_system({axiom_k, axiom_s}, {infer_mp})

# automatically fill in the conclusion for modus ponens
apply_mp = smart_infer(infer_mp)


def test_prove(theorem, proof, deduction):
    # here's where the work happens
    proven = verify_proof(proof, deduction)

    # check if the proof is valid
    assert proven

    # check if the proof proves the right theorem
    if theorem == proven:
        print(f'proved: {pretty_print(theorem)}')
        print('QED.')
    else:
        print(f'tried to prove: {pretty_print(theorem)}')
        print(f'instead proved: {pretty_print(proven)}')
        raise ValueError()


def tests_basic():
    from pattern_match import match

    assert not match(('P', 'P'), lambda x, y: (x, y, x))
    assert match(axiom_k('P', 'Q'), axiom_k)
    assert match(axiom_s('P', 'Q', 'R'), axiom_s)
    assert apply_mp(axiom(to('P', 'Q')), axiom('P'))

def test_prove_k():
    theorem = chain('P', 'Q', 'P')

    proof = axiom_k('P', 'Q')

    test_prove(theorem, proof, hilbert_ks)

def test_prove_kk():
    theorem = chain('P', 'Q', 'R', 'Q')

    k1 = axiom_k(chain('Q', 'R', 'Q'), 'P')
    k2 = axiom_k('Q', 'R')

    proof = apply_mp(k1, k2)

    test_prove(theorem, proof, hilbert_ks)

def test_prove_skk():
    # formula to prove: P -> P
    theorem = to('P', 'P')

    # Proof approach:
    # SKK
    # S = (P -> (Q -> P) -> P) -> (P -> Q -> P) -> P -> P
    # = K1 -> K2 -> P -> P

    a = c = 'P'
    _ = 'Q'
    b = to(_, 'P')

    s = axiom_s(a, b, c)
    k1 = axiom_k(a, b)
    k2 = axiom_k(a, _)

    sk1 = apply_mp(s, k1)
    sk1k2 = apply_mp(sk1, k2)

    proof = sk1k2

    test_prove(theorem, proof, hilbert_ks)


def main():
    tests_basic()
    test_prove_k()
    test_prove_kk()
    test_prove_skk()


if __name__ == '__main__':
    main()

