import dataclasses as D

import typing as T

from propositions import Term, Bottom, Variable


class Unsolvable(Exception):
    pass


def decompose(term: Term) -> tuple[type, tuple]:
    return type(term), tuple(getattr(term, field.name) for field in D.fields(term))


def get_vars(term) -> set[Variable]:
    if isinstance(term, Variable):
        return {term}

    variables = set()

    _, params = decompose(term)
    for param in params:
        if isinstance(param, Term):
            variables |= get_vars(param)

    return variables


def is_free(var, term) -> bool:
    return var not in get_vars(term)


Substitutions = dict[Variable, Term]


def substitute(term: Term, substitutions: Substitutions) -> Term:
    if isinstance(term, Variable):
        term = substitutions.get(term, term)

    if isinstance(term, Variable) and term in substitutions:
        raise ValueError("chained substitution detected")

    cls, params = decompose(term)
    params = list(params)

    for i, param in enumerate(params):
        if isinstance(param, Term):
            params[i] = substitute(param, substitutions)

    return cls(*params)


def unify(equations: set[tuple[Term, Term]]):
    # these are solved equations
    # they take the form v = t, where v is free in t
    substitutions: Substitutions = {}

    # these are unsolved equations
    # they can take any form
    unsolved = equations

    # repeat until the set of unsolved equations is empty
    while unsolved:
        # get the next unsolved equation
        lhs, rhs = unsolved.pop()

        # apply currently known substitutions
        lhs = substitute(lhs, substitutions)
        rhs = substitute(rhs, substitutions)

        match [lhs, rhs]:
            case _ if lhs == rhs:
                # if it's trivial (x = x), ignore it
                continue

            case [Variable() as x, _ as t] | [_ as t, Variable() as x]:
                # if it's x = t or t = x, this is a potential substitution

                # occurs check: x must be free in t, otherwise it's an infinite term
                if not is_free(x, t):
                    raise Unsolvable()

                # thanks to substitute(), x is new and t is already expanded
                # this works even when t is also a variable
                substitutions[x] = t

            case _:
                # the remaining case is f(*x) = g(*y)
                # for two trees to match, their roots and children must match
                f, x = decompose(lhs)
                g, y = decompose(rhs)

                # roots must match: f = g
                # in this case, f and g are type constants, so direct comparison works
                if f != g:
                    raise Unsolvable()

                # children must match: x_1 = y_1, x_2 = y_2, etc.
                # these can have any form, so they go back into the system of equations
                for x_i, y_i in zip(x, y):
                    unsolved.add((x_i, y_i))

    # if all goes well (i.e. the system is solvable), it yields a set of substitutions
    # this terminates because each step reduces the total # of tree nodes in unsolved

    # postcondition: the substitutions satisfy the original system of equations
    for lhs, rhs in equations:
        lhs = substitute(lhs, substitutions)
        rhs = substitute(rhs, substitutions)

        if lhs != rhs:
            raise AssertionError("equation unsatisfied")

    return substitutions


def relabel(term: Term, start_index: int = 0) -> Term:
    src = tuple(get_vars(term))
    substitutions = {}

    for offset, variable in enumerate(src):
        substitutions[variable] = Variable(start_index + offset)

    return substitute(term, substitutions)


def verify(term: Term, axioms: tuple[Term]):
    for axiom in axioms:
        try:
            substitutions = unify({(term, axiom)})
        except Unsolvable:
            pass

    return False
