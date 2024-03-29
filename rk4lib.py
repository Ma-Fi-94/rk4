"""A convenience lib for interacting with the rk4.so a bit more easily."""

from ctypes import CDLL, CFUNCTYPE, POINTER, c_double, c_int, cast
from typing import Callable, List, Tuple

# Load the SO using the ctypes library
rk4 = CDLL("./rk4.so")

# Annotate the solver function for later calling
solve = rk4.solve
fun_type = CFUNCTYPE(None, c_double, POINTER(c_double), POINTER(c_double))
solve.argtypes = [fun_type, POINTER(c_double), c_double, c_double, c_int]
solve.restype = POINTER(POINTER(c_double))

# Annotate the dealloc function for later calling
dealloc = rk4.dealloc
dealloc.argtypes = [POINTER(POINTER(c_double)), c_int]
dealloc.restype = None

def integrate(fun: Callable[[float, List[float]],
                            List[float]], y0: List[float], dt: float,
              tmax: float) -> Tuple[List[float], List[List[float]]]:
    """Perform numerical integration of the function fun
    with intial condition y0 from t=[0; tmax] with time step dt. """

    # Check types of all params
    if not callable(fun):
        raise TypeError("Parameter fun must be a callable.")

    try:
        y0 = list(y0)
    except TypeError as exc:
        raise TypeError("Parameter y0 must be list of args to f.") from exc

    try:
        dt = float(dt)
    except ValueError as exc:
        raise ValueError("Parameter dt must be a float") from exc

    try:
        tmax = float(tmax)
    except ValueError as exc:
        raise ValueError("Parameter tmax must be a number.") from exc

    # Check that fun has the appropriate signature and accepts y0 to return dydt
    try:
        dydt = fun(0, y0)
    except IndexError as exc:
        raise TypeError("Function fun(t, y) incompatible with y0.") from exc

    # Check that fun returns a list
    try:
        dydt = list(dydt)
    except ValueError as exc:
        raise TypeError("Function fun(t,y) does not return list.") from exc


    # We get a Python function fun(t, y) -> dydt.
    # We need to make a new function as callback for the C shared object,
    # which writes to an outparam instead: ext_fun(t, y, dydt) -> None
    @CFUNCTYPE(None, c_double, POINTER(c_double), POINTER(c_double))
    def ext_fun(t, y, dydt):
        # We really need this explicit loop over all dimensions.
        # Otherwise, we'd get only zeros.
        for i in range(len(y0)):
            dydt[i] = fun(t, y)[i]

    # Convert the other parameters to c_types, so that we may pass them
    ext_dt = c_double(dt)
    ext_tmax = c_double(tmax)
    ext_y0 = cast((c_double * len(y0))(*y0), POINTER(c_double))
    ext_d = c_int(len(y0))

    # Calling the function, getting a double** as return
    ext_ret = solve(ext_fun, ext_y0, ext_dt, ext_tmax, ext_d)

    # Copy results to Python variables for returning
    t = ext_ret[0][0:int(tmax / dt)]
    sol = []
    for i in range(len(y0)):
        sol.append(ext_ret[i + 1][0:int(tmax / dt)])

    # Dealloc the memory allocated in the SO
    dealloc(ext_ret, len(y0))

    # Return results as tuple of time points and system variables
    return t, sol
