"""Test suite for the convenience library rk4.py"""

from rk4lib import integrate
import numpy as np

def test_solve_expdecay():
    """Test solver with a simple exponential decay model."""
    
    def expdecay(t, y):
        return [-0.1*y[0]]
    
    t, sol = integrate(fun=expdecay,
                       y0=[100.0],
                       dt=1e-6,
                       tmax=1.0)
    
    # Assert that numerical solution is close to analytical solution
    assert np.abs(sol[0][-1] - 100.0*np.exp(-0.1*1.0)) < 1e-3
    

def test_solve_lorenz():
    """Test solver with the Lorenz system."""
    
    def lorenz(t, y):
        dydt_0 = 10.0 * (y[1] - y[0])
        dydt_1 = y[0] * (28.0 - y[2]) - y[1]
        dydt_2 = y[0] * y[1] - (8.0 / 3.0) * y[2]
        return [dydt_0, dydt_1, dydt_2]
    
    t, sol = integrate(fun=lorenz,
                       y0=[1.0, 1.0, 1.0],
                       dt=1e-6,
                       tmax=1.0)
