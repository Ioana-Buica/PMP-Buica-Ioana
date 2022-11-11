
import arviz as az
import matplotlib.pyplot as plt

import numpy as np
import pymc3 as pm
import pandas as pd

if __name__ == "__main__":

    data = pd.read_csv('Prices.csv')

    price = data['Price'].values
    speed = data['Speed'].values
    hardDrive = data['HardDrive'].values
    ram = data['Ram'].values
    premium = data['Premium'].values
    
    fig, axes = plt.subplots(2, 2, sharex=False, figsize=(10, 8))
    axes[0,0].scatter(speed, price, alpha=0.6)
    axes[0,1].scatter(hardDrive, price, alpha=0.6)
    axes[1,0].scatter(ram, price, alpha=0.6)
    axes[1,1].scatter(premium, price, alpha=0.6)
    axes[0,0].set_ylabel("Price")
    axes[0,0].set_xlabel("Speed")
    axes[0,1].set_xlabel("HardDrive")
    axes[1,0].set_xlabel("Ram")
    axes[1,1].set_xlabel("Premium")
    #plt.savefig('price_correlations.png')

    # x1 este frecvenţa procesorului
    X1 = speed
    X1_mean = X1.mean(axis=0, keepdims=True)
    X1_centered = X1 - X1_mean

    # x2 este logaritmul (natural) al mărimii hard diskului.
    X2 = np.log(hardDrive)
    X2_mean = X2.mean(axis=0, keepdims=True)
    X2_centered = X2 - X2_mean

    with pm.Model() as model_mlr:
        α_tmp = pm.Normal('α_tmp', mu=0, sd=10)
        sigma = pm.HalfNormal('sigma', sd=1)

        β1 = pm.Normal('β1', mu=0, sd=1)
        β2 = pm.Normal('β2', mu=0, sd=1)

        # μ  =  pm.Deterministic('μ',α + β1*X1 +  β2*X2 )
        μ = α_tmp + pm.math.dot(X1_centered, β1) + pm.math.dot(X2_centered, β2)

        
        α = pm.Deterministic('α', α_tmp - pm.math.dot(X1_mean, β1) - pm.math.dot(X2_mean, β2))

        data_price = pm.Normal('data_price', 
                                mu=μ, 
                                sd=sigma, 
                                observed=price)

        trace = pm.sample(200, return_inferencedata=True)
        # trace = pm.sample(20000, tune=20000, cores=4)

    # az.plot_trace(trace, var_names=['α', "β1", "β2", "sigma"])
    az.plot_posterior(trace, var_names=['α', "β1", "β2", "sigma"])


    # ex2 - az.plot_posterior / sample(return_inferencedata=True)