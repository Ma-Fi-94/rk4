"""Test suite for the convenience library rk4.py, which abstracts
away the nitty gritty details of how to interact with the shared
object rk4.so implemented in C."""

from rk4lib import integrate

def test_solve():
    """Test the main function of the convenience library."""
    
    # A function we want to solve
    def lorenz(t, y):
        dydt_0 = 10.0 * (y[1] - y[0])
        dydt_1 = y[0] * (28.0 - y[2]) - y[1]
        dydt_2 = y[0] * y[1] - (8.0 / 3.0) * y[2]
        return [dydt_0, dydt_1, dydt_2]
    
    t, sol = integrate(fun=lorenz,
                       y0=[1.0, 1.0, 1.0],
                       dt=1e-6,
                       tmax=1.0)
    
    pass
