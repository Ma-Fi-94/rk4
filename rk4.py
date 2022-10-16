"""A convenience lib for interacting with the rk4.so a bit more easily."""

from ctypes import CDLL, CFUNCTYPE, POINTER, c_double, c_int, cast
from typing import Callable, List, Tuple

# Load the SO using the ctypes library
LIBNAME = "./rk4.so"
c_lib = CDLL(LIBNAME)

# Annotate solve function for later calling
# double** solve(void (*f)(double, double*, double*), double* y0, double dt, double tmax, int d)
solve = c_lib.solve
solve.restype = POINTER(POINTER(c_double))
solve.argtypes = [
    CFUNCTYPE(None, c_double, POINTER(c_double), POINTER(c_double)),
    POINTER(c_double), c_double, c_double, c_int
]

# Annotate dealloc function for later calling
# void dealloc(double** ptr, int d)
dealloc = c_lib.dealloc
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
        raise TypeError(
            "Parameter y0 must be a list of arguments to f.") from exc
    try:
        dt = float(dt)
    except TypeError as exc:
        raise TypeError("Parameter dt must be a float") from exc
    try:
        tmax = float(tmax)
    except TypeError as exc:
        raise TypeError(
            "Parameter tmax must be a list of arguments to f.") from exc

    # Check that fun has the appropriate signature and takes y0 to return dydt
    try:
        dydt = fun(0, y0)
        dydt = list(dydt)
    except TypeError as exc:
        raise TypeError(
            "Parameter fun must be a function fun(t, y0) -> dydt.") from exc

    # TODO: We need to make a CFUNCTYPE(None, c_double, POINTER(c_double), POINTER(c_double))(f)
    # In particular, fun returns dydt, but for the rk4.so we require
    # a function ext_fun which writes to an "outparameter"
    ext_fun = fun

    # Convert the other parameters to c_types, so that we may pass them
    ext_dt = c_double(dt)
    ext_tmax = c_double(tmax)
    ext_y0 = (c_double * len(y0))(*y0)
    ext_y0 = cast(ext_y0, POINTER(c_double))
    ext_d = c_int(len(y0))

    # Calling the function, getting a double** as return
    ret = solve(ext_fun, ext_y0, ext_dt, ext_tmax, ext_d)

    # TODO: copy results to a Python variable and dealloc memory allocated in the SO
    # ...

    # TODO: return results as a tuple (t, y)
    return ret
