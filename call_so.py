# Need this for calling the SO
import ctypes
from ctypes import *

# Load the shared library into ctypes
libname = "./rk4.so"
c_lib = ctypes.CDLL(libname)

############################################


# Want to call:
# double** solve(void (*f)(double, double*, double*), double* y0, double dt, double tmax, int d)
solve = c_lib.solve
solve.restype = POINTER(POINTER(c_double))
solve.argtypes = [CFUNCTYPE(None, c_double, POINTER(c_double), POINTER(c_double)), POINTER(c_double), c_double, c_double, c_int]

# We want to pass this Pyton function to the solver, thus we need to properly annotate it
@CFUNCTYPE(None, c_double, POINTER(c_double), POINTER(c_double))
def lorenz(t, y, dydt):
    dydt[0] = 10.0*(y[1]-y[0])
    dydt[1] = y[0]*(28.0-y[2]) - y[1]
    dydt[2] = y[0]*y[1] - (8.0/3.0)*y[2]


# The params
y0 = (c_double*3)(1,2,3)
y0 = cast(y0, POINTER(c_double))

dt = c_double(0.0001)
tmax = c_double(10.0)
d = c_int(3)

# Calling the function, getting a double** as return
ret = solve(lorenz, y0, dt, tmax, d)

# do stuff with ret
print(ret[0][0:100])
print(ret[1][0:100])

# dealloc in C, to avoid leak
dealloc = c_lib.dealloc
dealloc.argtypes = [POINTER(POINTER(c_double)), c_int]
dealloc.restype = None
dealloc(ret, 3)





