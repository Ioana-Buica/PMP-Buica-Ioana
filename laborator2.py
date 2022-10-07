import numpy as np
from scipy import stats

import matplotlib.pyplot as plt
import arviz as az

np.random.seed(1)

λ1 = 1/4
λ2 = 1/6 

primul = stats.expon.rvs(0,1/λ1,10000)
doilea = stats.expon.rvs(0,1/λ2,10000)
# doilea = primul + 1/5 primul

# Generaţi 10000 de valori pentru X
x = stats.norm.rvs(0, 1, size=10000) 
# Distributie normala cu media 0 si deviatie standard 1, 1000 samples

y = stats.uniform.rvs(-1, 2, size=10000) 
# Distributie uniforma intre -1 si 1, 1000 samples . 
# Primul parametru fiind limita inferioara a intervalului, 
# al doilea parametru fiind "marimea" intervalului, aka [-1,-1+2] = [-1,1] 

z = 0.4*primul +0.6*doilea # Compunerea prin insumare a celor 2 distributii

az.plot_posterior({'a':primul,'b':doilea,'z':z}) # Afisarea aproximarii densitatii probabilitatilor, mediei, intervalului etc. variabilelor x,y,z
plt.show() 