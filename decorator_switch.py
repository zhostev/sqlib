def simple_decorator(func):
    def wrapper(*args, **kwargs):
        if __name__ == '__main__':
            print("simple_decorator")
        return func(*args, **kwargs)
    return wrapper


def decorator_with_parameters(print_func=False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if __name__ == '__main__':
                print("decorator_with_parameters")
            if print_func:
                print(f'{func = }')
            return func(*args, **kwargs)
        return wrapper
    return decorator


def second_order_decorator(sub_dec, *args, enabled=False, **kwargs):
    def wrapper(func):
        if enabled:
            if __name__ == '__main__':
                print("switchable_decorator")
            if args or kwargs:
                return sub_dec(*args, **kwargs)(func)
            else:
                return sub_dec(func)
        else:
            return func
    return wrapper   


@second_order_decorator(simple_decorator, enabled=True)
def my_function0():
    print("my function 0\n")


@second_order_decorator(decorator_with_parameters, enabled=True, print_func=True)
def my_function1():
    print("my function 1\n")
    

@second_order_decorator(decorator_with_parameters, enabled=False, print_func=True)
def my_function2():
    print("my function 2\n")


@simple_decorator
def my_function3():
    print("my function 3\n")


@decorator_with_parameters(print_func=True)
def my_function4():
    print("my function 4\n")


if __name__ == '__main__':
    my_function0()
    my_function1()
    my_function2()
    my_function3()
    my_function4()