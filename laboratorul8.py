import pymc3 as pm
import numpy as np
import pandas as pd
import theano.tensor as tt
# import seaborn as sns
import scipy.stats as stats
from scipy.special import expit as logistic
import matplotlib.pyplot as plt
import arviz as az

if __name__ == "__main__":

    data = pd.read_csv('Admission.csv')

    admission = data['Admission'].values
    gre = data['GRE'].values
    gpa = data['GPA'].values

    y_1 = pd.Categorical(data['Admission']).codes
    x_n = ['GRE', 'GPA']
    x_1 = data[x_n].values  

    with pm.Model() as model_0:
        α = pm.Normal('α', mu=0, sd=10)
        β = pm.Normal('β', mu=0, sd=2, shape=len(x_n)+1)

        μ = α + pm.math.dot(gpa, β[0]) + pm.math.dot(gre, β[1])
        θ = pm.Deterministic('θ', 1 / (1 + pm.math.exp(-μ)))
        bd = pm.Deterministic('bd', -α/β[1] - β[0]/β[1] * gpa)

        yl = pm.Bernoulli('yl', p=θ, observed=y_1)
        idata_1 = pm.sample(2000, target_accept=0.9, return_inferencedata=True)

    #az.plot_posterior(idata_1)
    #plt.savefig('idata_1.png')

    idx = np.argsort(gpa)
    bd = idata_1.posterior['bd'].mean(("chain", "draw"))[idx]
    
    plt.scatter(gpa, gre, c=[f'C{x}' for x in y_1])
    plt.plot(gpa[idx], bd, color='k')

    az.plot_hdi(gpa, idata_1.posterior['bd'],  hdi_prob=0.94, color='k')

    plt.xlabel(x_n[0])
    plt.ylabel(x_n[1])

    plt.savefig('Granita_de_decizie.png')

    gpa = [3.5]
    gre = [550]

    ppc = pm.sample_posterior_predictive(idata_1, 2000, model=model_0)
    y_ppc = ppc['yl'][:, 0]

    grid, pdf = az.kde(y_ppc)
    az.plot_hdi(grid, pdf, hdi_prob=0.90)

    plt.xlabel('Admission')
    plt.yticks([])

    plt.savefig('Admission_ex3.png')

    gpa = [3.2]
    gre = [500]

    ppc = pm.sample_posterior_predictive(idata_1, 2000, model=model_0)
    y_ppc = ppc['yl'][:, 0]

    grid, pdf = az.kde(y_ppc)
    az.plot_hdi(grid, pdf, hdi_prob=0.90)

    plt.xlabel('Admission')
    plt.yticks([])

    plt.savefig('Admission_ex4.png')

    # ex4: Rezultatele optinute sunt in functie de datele cu care
    # s-a atrenat modelul