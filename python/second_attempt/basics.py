__all__ = ('axiom', 'inference', 'deductive_system')


def axiom(statement):
    return ('axiom', statement)

def inference(premises, conclusion):
    return ('infer', premises, conclusion)

def deductive_system(axioms, rules):
    return ('deductive', axioms, rules)
