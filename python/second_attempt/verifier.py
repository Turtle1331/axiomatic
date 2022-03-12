__all__ = ('verify_proof',)


from pattern_match import *
from functional import *

from basics import *


@check_wrap
def verify_proof(proof, deduction):
    axioms, rules = check_result(match(deduction, deductive_system))

    @in_case(inference)
    def on_inference(lemmas, conclusion):
        premises = tuple(map(lambda lemma: verify_proof(lemma, deduction), lemmas))
        infer_concrete = inference(premises, conclusion)

        if any(match(infer_concrete, rule) for rule in rules):
            return conclusion

    @in_case(axiom)
    def on_axiom(statement):
        axiom_concrete = axiom(statement)

        for ax in axioms:
            if match(axiom_concrete, ax) is not None:
                return statement

    return do_match(proof, on_inference, on_axiom)
