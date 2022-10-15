"""A convenience lib for interacting with the rk4.so a bit more easily.""" 

from ctypes import *
from typing import Callable, List, Tuple

# Load the SO using the ctypes library
libname = "./rk4.so"
c_lib = CDLL(libname)

# Annotate solve function for later calling
# double** solve(void (*f)(double, double*, double*), double* y0, double dt, double tmax, int d)
solve = c_lib.solve
solve.restype = POINTER(POINTER(c_double))
solve.argtypes = [CFUNCTYPE(None, c_double, POINTER(c_double), POINTER(c_double)),
                  POINTER(c_double),
                  c_double,
                  c_double,
                  c_int]

# Annotate dealloc function for later calling
# void dealloc(double** ptr, int d)
dealloc = c_lib.dealloc
dealloc.argtypes = [POINTER(POINTER(c_double)), c_int]
dealloc.restype = None

def integrate(f: Callable,
              y0: List[float],
              dt: float,
              tmax: float) -> Tuple[List[float], List[List[float]]]:
    
    # We can infer d from y0
    # TODO: However, it would be cool do doublecheck this with f
    d = c_int(len(y0))
    # ...
    
    # TODO: We need to make a CFUNCTYPE(None, c_double, POINTER(c_double), POINTER(c_double))(f)
    # In particular, f returns dydt, but for the rk4.so we require
    # a function which writes to an "outparameter"
    # ...
    
    # The other params
    dt = c_double(dt)
    tmax = c_double(tmax)
    y0 = (c_double*len(y0))(*y0)
    y0 = cast(y0, POINTER(c_double))

    # Calling the function, getting a double** as return
    ret = solve(lorenz, y0, dt, tmax, d)
    
    # TODO: copy results to a Python variable and dealloc memory allocated in the SO
    # ...
    
    # TODO: return results as a tuple (t, y)
    return





