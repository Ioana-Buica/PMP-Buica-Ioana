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
# Distribuţia Γ(α, λ) se poate apela cu stats.gamma(α,0,1/λ)

λ = 4
latenta = stats.expon.rvs(0, 1/λ, 1000)

unu   = stats.gamma.rvs( 4 ,0,1/3, size=1000) + latenta
doi   = stats.gamma.rvs( 4 ,0,1/2, size=1000) + latenta
trei  = stats.gamma.rvs( 5 ,0,1/2, size=1000) + latenta
patru = stats.gamma.rvs( 5 ,0,1/3, size=1000) + latenta

# către primul server cu probabilitatea 0.25,
# către al doilea cu probabilitatea 0.25, 
# 0.50
# iar către al treilea server cu probabilitatea 0.30.
# patru cu 0.20

rezultat = 0.25*unu + 0.25*doi + 0.30*trei + 0.20*patru

# az.plot_posterior({'l':latenta, 'a':unu, 'b':doi, 'c':trei, 'd':patru})
# az.plot_posterior({'r':rezultat}) 

# plt.show() 
# -------------------------------------------------------------------

# Random variates
# una nemăsluită 0.5/0.5
bn1 = stats.binom.rvs(n=1, p=0.5, size=10)

# cealaltă cu probabilitatea de 0.3 de a obţine stemă
bn2 = stats.binom.rvs(n=1, p=0.3, size=10)

# cealaltă cu probabilitatea de 0.7 
bn3 = stats.binom.rvs(n=1, p=0.7, size=10)

# ss
bnSS = bn1*bn2

# sb
bnSB = bn1*bn3

# bb
bnBB = bn1*bn3

# bs
bnBS = bn1*bn2

az.plot_posterior({'ss':bnSS, 'sb':bnSB, 'bb':bnBB, 'bs':bnBS}) 
plt.show()









