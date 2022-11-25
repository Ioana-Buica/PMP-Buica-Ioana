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

        μ = α + pm.math.dot(gpa, β[0]) + pm.math.dot(gre, β[0])
        θ = pm.Deterministic('θ', 1 / (1 + pm.math.exp(-μ)))

        bd = pm.Deterministic('bd', -α/β[1] - β[0]/β[1] * x_1[:,0])
        yl = pm.Bernoulli('yl', p=θ, observed=y_1)

        idata_1 = pm.sample(2000, target_accept=0.9, return_inferencedata=True)

    az.plot_posterior(idata_1)