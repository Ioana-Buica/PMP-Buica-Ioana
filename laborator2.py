import numpy as np
from scipy import stats

import matplotlib.pyplot as plt
import arviz as az

λ1 = 4
λ2 = 6 

primul = stats.expon.rvs(0,1/λ1,10000)
doilea = stats.expon.rvs(0,1/λ2,10000)

rezultat = 40/100 * primul + 60/100 * doilea

# az.plot_posterior({'a':primul, 'b':doilea, 'r':rezultat}) 
# plt.show() 

# ------------------------------------------

# Γ( 4,3 ) - gamma stats.gamma(α,0,1/λ)

λ1 = 4

unu   = stats.gamma.rvs( 4.3 ,0,1/λ1, size=1000)
doi   = stats.gamma.rvs( 4.2 ,0,1/λ1, size=1000)
trei  = stats.gamma.rvs( 5.2 ,0,1/λ1, size=1000)
patru = stats.gamma.rvs( 5.3 ,0,1/λ1, size=1000)

# către primul server cu probabilitatea 0.25,
# către al doilea cu probabilitatea 0.25, 
# 0.50
# iar către al treilea server cu probabilitatea 0.30.
# patru cu 0.20

rezultat = 0.25*unu + 0.25*doi + 0.30*trei + 0.20*patru

# az.plot_posterior({'a':unu, 'b':doi, 'c':trei, 'd':patru, 'r':rezultat}) 
# plt.show() 

# -------------------------------------------------------------------

# x = stats.norm.rvs(0, 1, size=10000)

# az.plot_posterior({'x':x}) #,'y':y,'z':z}) # Afisarea aproximarii densitatii probabilitatilor, mediei, intervalului etc. variabilelor x,y,z
# plt.show() 

from scipy.stats import bernoulli

# np.random.seed(42)

coin_flip = stats.bernoulli.rvs(0.30, 0, size=10)
print(coin_flip)

y1 = bernoulli.ppf(coin_flip, 0, 7) 
plt.plot(coin_flip, y1, "*") 

plt.show() 










