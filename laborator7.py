from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt

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
    
    """fig, axes = plt.subplots(2, 2, sharex=False, figsize=(10, 8))
    axes[0,0].scatter(speed, price, alpha=0.6)
    axes[0,1].scatter(hardDrive, price, alpha=0.6)
    axes[1,0].scatter(ram, price, alpha=0.6)
    axes[1,1].scatter(premium, price, alpha=0.6)
    axes[0,0].set_ylabel("Price")
    axes[0,0].set_xlabel("Speed")
    axes[0,1].set_xlabel("HardDrive")
    axes[1,0].set_xlabel("Ram")
    axes[1,1].set_xlabel("Premium")"""
    #plt.savefig('price_correlations.png')

    Y  = price

    # x1 este frecvenţa procesorului
    X1 = speed

    # x2 este logaritmul (natural) al mărimii hard diskului.
    X2 = np.log(hardDrive)
    # X2 = hardDrive

    with pm.Model() as model_RLM:
        α = pm.Normal('α', mu=0, sd=10)
        β1 = pm.Normal('β1', mu=0, sigma=10)
        β2 = pm.Normal('β2', mu=0, sd=10)

        ε = pm.HalfCauchy('ε', 5)

        μ = β1*X1 + β2*X2 + α

        y_pred = pm.Normal( 'y_pred',
                            mu = μ, 
                            sd = ε, 
                            observed = Y)

        samples = pm.sample(
                            init='advi+adapt_diag',
                            return_inferencedata=True)

    #az.plot_posterior(samples)
    
    #az.plot_trace(samples, var_names=['α', 'β1', 'β2', 'ε'])
    #az.summary(samples, var_names=['α', 'β1', 'β2', 'ε'])

    az.plot_forest( samples,
                    model_names=['model_RLM'],
                    var_names=['β1', 'β2'],
                    combined=False, colors='cycle', 
                    figsize=(8, 3))

    # ex 3 - Nu sunt predictori utili ai preţului de vânzare
    plt.scatter(X1, X2)

    plt.show()
   