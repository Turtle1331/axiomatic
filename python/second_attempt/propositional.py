__all__ = ('to', 'chain', 'pretty_print')


from pattern_match import *


def to(a, b):
    return ('implies', a, b)

def chain(head, *tail):
    if not tail:
        return head
    return to(head, chain(*tail))

def pretty_print(prop):
    @in_case(to)
    def on_implies(a, b):
        pa = pretty_print(a)
        pb = pretty_print(b)
        return f'{pa} -> {pb}'

    @default_case
    def default(x):
        return str(x)

    return do_match(prop, on_implies, default)


def main():
    print(pretty_print(chain('P', 'Q', 'R')))


if __name__ == '__main__':
    main()
