import pymc3 as pm
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import arviz as az
import random

if __name__ == '__main__':

    az.style.use('arviz-darkgrid')
    dummy_data = np.loadtxt('date.csv')

    x_1 = dummy_data[:, 0]
    y_1 = dummy_data[:, 1]

# ---- ex 2 ----------------------------------------------------
    while len(x_1) != 500:
        number = round(random.uniform(-1.081, 3.970), 3)
        x_1 = np.append(x_1,number)

    while len(y_1) != 500:
        number = round(random.uniform(-7.854, 9.357), 3)
        y_1 = np.append(y_1,number)

# --------------------------------------------------------------
    order = 5

    x_1p = np.vstack([x_1**i for i in range(1, order+1)]) 
    x_1s = (x_1p - x_1p.mean(axis=1, keepdims=True)) / x_1p.std(axis=1, keepdims=True)
    y_1s = (y_1 - y_1.mean()) / y_1.std()

    plt.scatter(x_1s[0], y_1s)
    plt.xlabel('x')
    plt.ylabel('y')
    
    plt.savefig('pct.png')
    plt.close()

    model_l = pm.Model()

    with pm.Model() as model_l:
        α = pm.Normal('α', mu=0, sd=1)
        β = pm.Normal('β', mu=0, sd=10)
        ε = pm.HalfNormal('ε', 5)
        μ = α + β * x_1s[0]
        y_pred = pm.Normal('y_pred', mu=μ, sd=ε, observed=y_1s)
        idata_l = pm.sample(2000, return_inferencedata=True)

    model_p = pm.Model()

    with pm.Model() as model_p:
        α = pm.Normal('α', mu=0, sd=1)
        β = pm.Normal('β', mu=0, sd=10, shape=order)
        ε = pm.HalfNormal('ε', 5)
        μ = α + pm.math.dot(β, x_1s)
        y_pred = pm.Normal('y_pred', mu=μ, sd=ε, observed=y_1s)
        idata_p = pm.sample(2000, return_inferencedata=True)

    x_new = np.linspace(x_1s[0].min(), x_1s[0].max(), 100)
    α_l_post = idata_l.posterior['α'].mean(("chain", "draw")).values
    β_l_post = idata_l.posterior['β'].mean(("chain", "draw")).values
    y_l_post = α_l_post + β_l_post * x_new

    plt.plot(x_new, y_l_post, 'C1', label='linear model')

    α_p_post = idata_p.posterior['α'].mean(("chain", "draw")).values
    β_p_post = idata_p.posterior['β'].mean(("chain", "draw")).values
    idx = np.argsort(x_1s[0])
    y_p_post = α_p_post + np.dot(β_p_post, x_1s)

    plt.plot(x_1s[0][idx], y_p_post[idx], 'C2', label=f'model order {order}')
    plt.scatter(x_1s[0], y_1s, c='C0', marker='.')
    plt.legend()

    plt.savefig('ex1a.png')
    plt.close()

# ---------------------- ex 1 b ---------------------------------------

    model_l_a = pm.Model()

    with pm.Model() as model_l_a:
        α = pm.Normal('α', mu=0, sd=1)
        β = pm.Normal('β', mu=0, sd=100)
        ε = pm.HalfNormal('ε', 5)
        μ = α + β * x_1s[0]
        y_pred = pm.Normal('y_pred', mu=μ, sd=ε, observed=y_1s)
        idata_l = pm.sample(2000, return_inferencedata=True)

    model_p_a = pm.Model()

    with pm.Model() as model_p_a:
        α = pm.Normal('α', mu=0, sd=1)
        β = pm.Normal('β', mu=0, sd=100, shape=order)
        ε = pm.HalfNormal('ε', 5)
        μ = α + pm.math.dot(β, x_1s)
        y_pred = pm.Normal('y_pred', mu=μ, sd=ε, observed=y_1s)
        idata_p_a = pm.sample(2000, return_inferencedata=True)

    x_new = np.linspace(x_1s[0].min(), x_1s[0].max(), 100)
    α_l_post = idata_l.posterior['α'].mean(("chain", "draw")).values
    β_l_post = idata_l.posterior['β'].mean(("chain", "draw")).values
    y_l_post = α_l_post + β_l_post * x_new

    plt.plot(x_new, y_l_post, 'C1', label='linear model')

    α_p_post = idata_p_a.posterior['α'].mean(("chain", "draw")).values
    β_p_post = idata_p_a.posterior['β'].mean(("chain", "draw")).values
    idx = np.argsort(x_1s[0])
    y_p_post = α_p_post + np.dot(β_p_post, x_1s)

    plt.plot(x_1s[0][idx], y_p_post[idx], 'C2', label=f'model order {order}')
    plt.scatter(x_1s[0], y_1s, c='C0', marker='.')
    plt.legend()

    plt.savefig('ex1b_1.png')
    plt.close()

    sd = np.array([10, 0.1, 0.1, 0.1, 0.1])

    model_l_b = pm.Model()

    with pm.Model() as model_l_b:
        α = pm.Normal('α', mu=0, sd=1)
        β = pm.Normal('β', mu=0, sd=sd)
        ε = pm.HalfNormal('ε', 5)
        μ = α + β * x_1s[0]
        y_pred = pm.Normal('y_pred', mu=μ, sd=ε, observed=y_1s)
        idata_l = pm.sample(2000, return_inferencedata=True)

    model_p_b = pm.Model()

    with pm.Model() as model_p_b:
        α = pm.Normal('α', mu=0, sd=1)
        β = pm.Normal('β', mu=0, sd=sd, shape=order)
        ε = pm.HalfNormal('ε', 5)
        μ = α + pm.math.dot(β, x_1s)
        y_pred = pm.Normal('y_pred', mu=μ, sd=ε, observed=y_1s)
        idata_p_b = pm.sample(2000, return_inferencedata=True)

    x_new = np.linspace(x_1s[0].min(), x_1s[0].max(), 100)
    α_l_post = idata_l.posterior['α'].mean(("chain", "draw")).values
    β_l_post = idata_l.posterior['β'].mean(("chain", "draw")).values
    y_l_post = α_l_post + β_l_post * x_new

    plt.plot(x_new, y_l_post, 'C1', label='linear model')

    α_p_post = idata_p_b.posterior['α'].mean(("chain", "draw")).values
    β_p_post = idata_p_b.posterior['β'].mean(("chain", "draw")).values
    idx = np.argsort(x_1s[0])
    y_p_post = α_p_post + np.dot(β_p_post, x_1s)

    plt.plot(x_1s[0][idx], y_p_post[idx], 'C2', label=f'model order {order}')
    plt.scatter(x_1s[0], y_1s, c='C0', marker='.')
    plt.legend()

    plt.savefig('ex1b_2.png')
    plt.close()