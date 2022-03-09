from inspect import signature



def unify(lhs, rhs, vars):
    assign = {}
    def _unify(lhs, rhs):
        if lhs in vars:
            return assign.setdefault(lhs, rhs) == rhs
        elif isinstance(lhs, str):
            return lhs == rhs
        elif isinstance(lhs, tuple) and isinstance(rhs, tuple):
            return all(_unify(*pair) for pair in zip(lhs, rhs))
        return False
    
    if _unify(lhs, rhs) and frozenset(assign.keys()) == frozenset(vars):
        return assign
    return None



def get_arity(fun):
    return fun.arity if hasattr(fun, 'arity') else len(signature(fun).parameters)

def simple_unify(instance, template):
    vars = tuple(object() for _ in range(get_arity(template)))
    pattern = template(*vars)
    
    assign = unify(pattern, instance, vars)
    
    if assign is not None:
        return tuple(assign[var] for var in vars)



def inference(premises, conclusion):
    return ('infer', premises, conclusion)


def split_inference(part):
    part_names = ('premises', 'conclusion')
    try:
        part_index = part_names.index(part)
    except ValueError:
        raise ValueError(f'part must be one of: {part_names}')
    
    def __outer__(fun):
        def __inner__(*args):
            res = fun(*args)
            parts = simple_unify(res, inference)
            if parts is not None:
                return parts[part_index]
        
        __inner__.arity = get_arity(fun)
        return __inner__
    
    return __outer__

get_premises = split_inference('premises')
get_conclusion = split_inference('conclusion')


def flatten_inference(lemma):
    conclusion = get_conclusion(lambda: lemma)()
    return conclusion if conclusion is not None else lemma

def apply_rule(rule, *lemmas):
    premises = tuple(map(flatten_inference, lemmas))
    values = simple_unify(premises, get_premises(rule))
    if values is not None:
        conclusion = get_conclusion(rule)(*values)
        return inference(lemmas, conclusion)



def match_axiom(instance, axiom):
    return simple_unify(instance, axiom) is not None

def match_inference(instance, rule):
    return simple_unify(instance, rule)




def deductive_system(axioms, rules):
    return ('deductive', axioms, rules)

def verify_proof(proof, deduction):
    axioms, rules = match_inference(deduction, deductive_system)
    
    infer_concrete = match_inference(proof, inference)
    if infer_concrete is not None:
        lemmas, conclusion = infer_concrete
        premises = tuple(verify_proof(lemma, deduction) for lemma in lemmas)
        infer_abstract = inference(premises, conclusion)
        
        for rule in rules:
            stuff = match_inference(infer_abstract, rule)
            if stuff is not None:
                return conclusion
    
    for axiom in axioms:
        if match_axiom(proof, axiom):
            return proof
    
    raise ValueError(proof)



def to(a, b):
    return ('implies', a, b)

def chain(head, *tail):
    if not tail:
        return head
    return to(head, chain(*tail))

def pretty_print(prop):
    implies = simple_unify(prop, to)
    if implies:
        a, b = map(pretty_print, implies)
        return f'({a} -> {b})'
    else:
        return str(prop)



def axiom_k(a, b):
    return chain(a, b, a)

def axiom_s(a, b, c):
    return chain(chain(a, b, c), to(a, b), a, c)

def infer_mp(a, b):
    return inference((to(a, b), a), b)

def apply_mp(ab, a):
    return apply_rule(infer_mp, ab, a)



def main():
    # sanity tests
    assert apply_mp(to('P', 'Q'), 'P')
    assert match_axiom(axiom_s('P', 'Q', 'R'), axiom_s)
    
    
    # allow K and S axioms and modus ponens inference rule
    deduction = deductive_system({axiom_k, axiom_s}, {infer_mp})
    
    
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
    
    proof = apply_mp(apply_mp(s, k1), k2)
    
    # sanity check
    assert proof
    
    # here's where the work happens
    proven = verify_proof(proof, deduction)
    
    
    if theorem == proven:
        print(f'proved: {pretty_print(theorem)}')
        print('QED.')
    else:
        print(f'tried to prove: {pretty_print(theorem)}')
        print(f'instead proved: {pretty_print(proven)}')


if __name__ == '__main__':
    main()

