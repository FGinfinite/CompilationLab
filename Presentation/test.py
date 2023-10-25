import fib
import time


def fib_py_recursion(n):
    if n < 2:
        return n
    else:
        return fib_py_recursion(n - 1) + fib_py_recursion(n - 2)


start = time.time()
print(fib.fib_recursion(35))
end = time.time()
print("cython:" + str((end - start)))

start = time.time()
print(fib_py_recursion(35))
end = time.time()
print("python:" + str((end - start)))
