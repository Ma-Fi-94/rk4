"""Test suite for the convenience library rk4.py, which abstracts
away the nitty gritty details of how to interact with the shared
object rk4.so implemented in C."""

from rk4lib import integrate
import numpy as np

def test_solve_expdecay():
    """Test the main function of the convenience library."""
    
    # A linear 1d ODE.
    def expdecay(t, y):
        return [-0.1*y[0]]
    
    # Solve numerically
    t, sol = integrate(fun=expdecay,
                       y0=[100.0],
                       dt=1e-6,
                       tmax=1.0)
    
    # Assert that numerical solution is close to analytical solution
    assert np.abs(sol[0][-1] - 100.0*np.exp(-0.1*1.0)) < 1e-3
    

def test_solve_lorenz():
    """Test the main function of the convenience library."""
    
    # A multidimensional, chaotic function, which is analytically unsolvable.
    def lorenz(t, y):
        dydt_0 = 10.0 * (y[1] - y[0])
        dydt_1 = y[0] * (28.0 - y[2]) - y[1]
        dydt_2 = y[0] * y[1] - (8.0 / 3.0) * y[2]
        return [dydt_0, dydt_1, dydt_2]
    
    t, sol = integrate(fun=lorenz,
                       y0=[1.0, 1.0, 1.0],
                       dt=1e-6,
                       tmax=1.0)
    
