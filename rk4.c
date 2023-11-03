#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

static inline void* safe_malloc(size_t size) {
    void* ptr = malloc(size);
    
    if (ptr == NULL) {
        fprintf(stdout, "Failed to allocate memory. Exiting.\n");
        exit(-1);
    }

    return(ptr);
}


static inline void lin_comb(double* res,
    double c1,
    double* vec1,
    double c2,
    double* vec2,
    int d) {

    for (int i = 0; i < d; i++) {
        res[i] = c1*vec1[i] + c2*vec2[i];
    }
}


double** solve(void (*f)(double, double*, double*),
    double* y0,
    double dt,
    double tmax,
    int d) {

    // Some precomputing
    long dt_half = dt/2;
    long i_max   = (long) (tmax/dt);
    int size_y   = d * sizeof(double);

    // For storing intermediate results
    double* k1    = (double*) safe_malloc(size_y);
    double* k2    = (double*) safe_malloc(size_y);
    double* k3    = (double*) safe_malloc(size_y);
    double* k4    = (double*) safe_malloc(size_y);
    double* y_tmp = (double*) safe_malloc(size_y);

    // Results to be stored here
    double** res = (double**) safe_malloc((1+d) * sizeof(double*));
    for (int i = 0; i < 1+d; i++) {
        res[i] = (double*) safe_malloc(i_max * sizeof(double));
    }

    // Init system state with initial condition
    double t  = 0;
    double* y = (double*) safe_malloc(size_y);
    memcpy(y, y0, size_y);
               
    // Main integration loop
    for (long i = 0; i < i_max; i++) {
        // Save current state
        res[0][i] = t;
        for (int j = 0; j < d; j++) {
            res[j+1][i] = y[j];
        }

        // k1 = f(t, y)
        f(t, y, k1);
        
        // k2 = f(t+dt/2, y+dt/2*k1)
        lin_comb(y_tmp, 1, y, dt_half, k1, d);
        f(t+dt_half, y_tmp, k2);
        
        // k3 = f(t+dt/2, y+dt/2*k2)        
        lin_comb(y_tmp, 1, y, dt_half, k2, d);        
        f(t+dt_half, y_tmp, k3);
        
        // k4 = f(t+dt, y+dt*k3)
        lin_comb(y_tmp, 1, y, dt, k3, d);                       
        f(t+dt, y_tmp, k4);
        
        // Integration step y := y+dt*(1/6)*(k1+2k2+2k3+k4), t := t+dt
        for (int j = 0; j < d; j++) {
            y[j] = y[j] + dt*(1.0/6.0)*(k1[j]+2*k2[j]+2*k3[j]+k4[j]);
        }
        t += dt;       
    }
    
    // Cleanup -- especially important if we call this function from python!
    free(y);
    free(k1);
    free(k2);
    free(k3);           
    free(k4);
    free(y_tmp);
    
    // Returning results
    return res;
    
}

// need to call this from Python ("dealloc(res)") to avoid leaks
void dealloc(double** ptr, int d) {
    for (int i = 0; i<d+1; i++) {
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
    double* y0 = (double*) safe_malloc(3 * sizeof(double));

    y0[0] = 1.0;
    y0[1] = 1.0;
    y0[2] = 1.0;

    solve(lorenz, y0, 0.001, 1000, 3);
    return 0;
}

