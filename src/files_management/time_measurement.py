from timeit import default_timer as timer


def benchmark(func):
    """
    It prints out:
        => the func name
        => elapsed time
        => *args
        => **kwargs

    :param func: given function to measure its performance.
    :return: A list that contains:
            [0]: the elapsed time.
            [i] for all i > 0: all the possible returned values of func.
    """
    def wrapper_timer(*args, **kwargs):
        start = timer()
        returned_values = func(*args, **kwargs)
        end = timer()
        elapsed_time = (end - start) * (10 ** 6)
        if returned_values is not None:
            stack_returned_values = list(returned_values)
        else:
            stack_returned_values = []
        stack_returned_values.insert(0, elapsed_time)
        args_info = get_function_args(*args)
        kwargs_info = get_function_kwargs(**kwargs)
        results = """
        Function benchmark:
        ->  Function name:\t{0}.
        ->  Elapsed time:\t{1} microseconds.
        """.format(func.__name__, elapsed_time)
        print(results+args_info+kwargs_info)
        return stack_returned_values
    return wrapper_timer


def get_function_args(*args):
    no_args = 0
    additional_info = ""
    if len(args) > no_args:
        additional_info += "Function args:\n\t\t"
        for i in range(0, len(args)):
            additional_info += "->  func arg[" + str(i) + "]:\t" + str(args[i]) + "\n\t\t"
    return additional_info


def get_function_kwargs(**kwargs):
    kwargs_info = ""
    if bool(kwargs):
        kwargs_info += "Function kwargs\n\t\t"
        for key, value in kwargs.items():
            kwargs_info += "-> func kwargs[" + str(key) + "]:\t" + str(value) + "\n\t\t"
    return kwargs_info
