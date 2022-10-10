#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

double** solve(void (*f)(double, double*, double*),
           double* y0,
           double dt,
           double tmax,
           int d) {
    
    // Init current system state with initial condition
    double t = 0;
    double* y = (double*) malloc(d * sizeof(double));
    memcpy(y, y0, d*sizeof(double));
    
    // Results to be stored here
    long imax = (long) (tmax/dt);
    double** res = (double**) malloc((1+d) * sizeof(double*));
    for (int i = 0; i < 1+d; i++) {
        res[i] = (double*) malloc(imax * sizeof(double));
    }
           
    // For storing the RK coefficients during iteration
    double* k1 = (double*) malloc(d * sizeof(double));
    double* k2 = (double*) malloc(d * sizeof(double));
    double* k3 = (double*) malloc(d * sizeof(double));
    double* k4 = (double*) malloc(d * sizeof(double));
    
    // For calculating y for the intermediate steps k2,k3,k4
    double* y_tmp = (double*) malloc(d * sizeof(double));
    
    // Performance hack for avoiding potential recalculation
    long dthalf = dt/2;
    
    // Main integration loop
    for (long i = 0; i < imax; i++) {
        // Save current state
        res[0][i] = t;
        for (int j = 0; j < d; j++) {
            res[j+1][i] = y[j];
        }
        
        // k1 = f(t, y)
        f(t, y, k1);
        
        // k2 = f(t+dt/2, y+dt/2*k1)
        for (int j = 0; j < d; j++) {
            y_tmp[j] = y[j] + dthalf*k1[j];
        }
        f(t+dthalf, y_tmp, k2);
        
        // k3 = f(t+dt/2, y+dt/2*k2)        
        for (int j = 0; j < d; j++) {
            y_tmp[j] = y[j] + dthalf*k2[j];
        }
        f(t+dthalf, y_tmp, k3);
        
        // k4 = f(t+dt, y+dt*k3)
        for (int j = 0; j < d; j++) {
            y_tmp[j] = y[j] + dt*k3[j];
        }       
        f(t+dt, y_tmp, k4);
        
        // Integration step y := y+dt*(1/6)*(k1+2k2+2k3+k4), t := t+dt
        for (int j = 0; j < d; j++) {
            y[j] = y[j] + dt*(1.0/6.0)*(k1[j]+k2[j]+k3[j]+k4[j]);
        }
        t += dt;       
    }
    
    return res;
    
}

// need to call this from Python ("dealloc(res)") to avoid leaks
void dealloc(double** ptr, int d) {
    for (int i = 0; i<d; i++) {
        free(ptr[i]);
    }
    free (ptr);
}

/////////////////////////////////////////////////////////////////////////////////
// All the stuff below this block is just for running the program on its own.
// It can be safely ignored if the code is to be used as a shared object.
/////////////////////////////////////////////////////////////////////////////////

void lorenz(double t, double* y, double* dydt) {
    // The Lorenz system as an example function to solve.   
    dydt[0] = 10.0*(y[1]-y[0]);
    dydt[1] = y[0]*(28.0-y[2]) - y[1];
    dydt[2] = y[0]*y[1] - (8.0/3.0)*y[2];
}


int main() {
    double* y0 = (double*) malloc(3 * sizeof(double));

    y0[0] = 1.0;
    y0[1] = 1.0;
    y0[2] = 1.0;

    solve(lorenz, y0, 0.001, 1000, 3);
    return 0;
}

