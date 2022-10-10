from inspect import getsource


if_ = lambda p, t, e: t() if p() else e()
loop = lambda c, e, ret=None: if_(c, lambda: (ret := e(), loop(c, e, ret))[1], lambda: ret)
fib = lambda n: if_(lambda: n <= 1, lambda: n, lambda: fib(n - 1) + fib(n - 2))
print("fibonacci of 10", fib(10))

func_name = lambda l: getsource(l).split("=")[0].strip()
trace = lambda f: lambda *args, **kwargs: (
    print(f"{func_name(f)}({args}, {kwargs}) called "),
    res := f(*args, **kwargs),
    print(f"{func_name(f)}() returned {res!r}"),
)[1]

fact = lambda n: if_(lambda: n > 1, lambda: n * fact(n - 1), lambda: 1)

fact_acc = lambda n, acc=1: if_(lambda: n > 1, lambda: fact_acc(n - 1, n * acc), lambda: acc)

identity = lambda v: v
fact_tail_optimized = lambda n, cont=identity: if_(
    lambda: n > 1,
    lambda: lambda: fact_tail_optimized(n - 1, lambda value: cont(n * value)),
    lambda: cont(1),
)
range = lambda n: if_(lambda: n < 0, lambda: [], lambda: range(n - 1) + [n])
range_acc = lambda n, acc=None: if_(
    lambda: n < 0, lambda: acc or [], lambda: range_acc(n - 1, [n] + (acc or []))
)


def trampoline(f, *args):
    r = f(*args)
    while callable(r):
        r = r()
    return r


trace(fact)(10)
trace(fact_acc)(10)
trampoline(fact_tail_optimized, 10)
