__all__ = ('match', 'in_case', 'default_case', 'do_match')


from inspect import signature


def unify(lhs, rhs, vars):
    assign = {}
    def _unify(lhs, rhs):
        if lhs in vars:
            return assign.setdefault(lhs, rhs) == rhs
        elif isinstance(lhs, str):
            return lhs == rhs
        elif isinstance(lhs, tuple) and isinstance(rhs, tuple):
            return len(lhs) == len(rhs) and all(_unify(*pair) for pair in zip(lhs, rhs))
        return False

    if _unify(lhs, rhs) and frozenset(assign.keys()) == frozenset(vars):
        return assign



def get_arity(fun):
    return fun.arity if hasattr(fun, 'arity') else len(signature(fun).parameters)

def match(instance, template):
    vars = tuple(range(get_arity(template)))
    pattern = template(*vars)

    assign = unify(pattern, instance, vars)

    if assign is not None:
        return tuple(assign[var] for var in vars)

def match_case(template, on_match):
    return ('match_case', template, on_match)

def in_case(template):
    def case(on_match):
        return match_case(template, on_match)

    return case

default_case = in_case(lambda x: x)

def do_match(instance, *cases):
    for case in cases:
        template, on_match = match(case, match_case)
        assign = match(instance, template)
        if assign:
            return on_match(*assign)

    raise ValueError(instance)
