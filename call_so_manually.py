# Need this for calling the SO
from ctypes import *

# Load the shared library into ctypes
libname = "./rk4.so"
c_lib = CDLL(libname)

# Want to call:
# double** solve(void (*f)(double, double*, double*), double* y0, double dt, double tmax, int d)
solve = c_lib.solve
solve.restype = POINTER(POINTER(c_double))
solve.argtypes = [
    CFUNCTYPE(None, c_double, POINTER(c_double), POINTER(c_double)),
    POINTER(c_double), c_double, c_double, c_int
]

############################################

# A simple 1d ODE which we can analytically solve to check the numerics

# We want to pass this Python function to the solver, thus we need to properly annotate it
@CFUNCTYPE(None, c_double, POINTER(c_double), POINTER(c_double))
def expdecay(t, y, dydt):
    dydt[0] = -0.1 * y[0]


# The params
y0 = (c_double * 1)(100.0)
y0 = cast(y0, POINTER(c_double))
dt = c_double(1e-6)
tmax = c_double(1.0)
d = c_int(1)

# Calling the function, getting a double** as return
ret = solve(expdecay, y0, dt, tmax, d)

# Print last value of numerical solution
y_final_num = ret[1][int(1.0/1e-6)-1]
print("y(1.0) numerical: ", y_final_num)

y_final_anal = 100*(2.71)**(1.0*(-0.1))
print("y(1.0) analytical: ", y_final_anal)

print("Difference num. vs. anal. solution:", (y_final_num-y_final_anal)/y_final_anal)

# dealloc in C, to avoid leak
dealloc = c_lib.dealloc
dealloc.argtypes = [POINTER(POINTER(c_double)), c_int]
dealloc.restype = None
dealloc(ret, 3)


############################################

# A more complex example: the 3d chaotic Lorenz system

# We want to pass this Python function to the solver, thus we need to properly annotate it
@CFUNCTYPE(None, c_double, POINTER(c_double), POINTER(c_double))
def lorenz(t, y, dydt):
    dydt[0] = 10.0 * (y[1] - y[0])
    dydt[1] = y[0] * (28.0 - y[2]) - y[1]
    dydt[2] = y[0] * y[1] - (8.0 / 3.0) * y[2]


# The params
y0 = (c_double * 3)(1, 2, 3)
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

