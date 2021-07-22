from timeit import default_timer as timer


def benchmark(func):
    def wrapper(*args, **kwargs):
        start = timer()
        val = func(*args, **kwargs)
        end = timer()
        NO_ARGS = 0
        additional_info = ""
        if len(args) > NO_ARGS:
            additional_info += "Function args:\n\t\t"
            i = 0
            for arg in args:
                additional_info += "->  func arg[" + str(i) + "]:\t" + str(arg) + ".\n\t\t"
                i += 1

        results = """
        Function benchmark:
        ->  Function name:\t{0}.
        ->  Elapsed time:\t{1} microseconds.
        """.format(func.__name__, (end-start)*(10**6))
        print(results+additional_info)
        return val

    return wrapper

"""
@benchmark
def f():
    res=0
    for i in range(1, 1000000):
       res +=i
    return res

f()
print(f())
"""