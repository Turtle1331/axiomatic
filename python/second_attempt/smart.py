__all__ = ('smart_infer',)


from pattern_match import *
from functional import *

from basics import *


def get_premises(infer):
    premises, conclusion = check_wrap(match)(infer, inference)
    return premises

def get_claim(proof):
    @in_case(inference)
    def on_inference(lemmas, conclusion):
        return conclusion

    @in_case(axiom)
    def on_axiom(statement):
        return statement

    return do_match(proof, on_inference, on_axiom)

def smart_infer(rule):
    @wraps(rule)
    def apply_rule(*lemmas):
        rule_premises = compose(get_premises)(rule)
        lemma_premises = tuple(map(get_claim, lemmas))

        assign = check_result(match(lemma_premises, rule_premises), 'apply_rule: could not match lemmas to rule premises')

        infer_abstract = rule(*assign)
        infer_premises, infer_conclusion = check_result(match(infer_abstract, inference))

        infer_concrete = inference(lemmas, infer_conclusion)
        return infer_concrete

    return apply_rule
