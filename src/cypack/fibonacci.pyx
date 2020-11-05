cpdef int fib(int n):
    """Non-recursively calculate the n'th Fibonacci number."""
    cdef int a = 0, b = 1
    cdef int i
    for i in range(n):
        a, b = b, a+b
    return a
