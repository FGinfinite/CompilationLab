def fib(n):
    """Print the Fibonacci series up to n."""
    a, b = 0, 1
    while b < n:
        print(b),
        a, b = b, a + b

def fib_recursion(n):
    """Print the Fibonacci series up to n."""
    if n < 2:
        return n
    else:
        return fib_recursion(n-1) + fib_recursion(n-2)