import numpy as np
from scipy import stats
import pymc3 as pm

import matplotlib.pyplot as plt
import arviz as az
import pandas as pd

if __name__ == '__main__':

    data1 = az.load_arviz_data("centered_eight")
    post = data1.posterior
    print(post)

    data2 = az.load_arviz_data("non_centered_eight")
    post = data2.posterior
    print(post['chain'])
    print(post['draw'])
    az.plot_posterior(data2)
    plt.show()

    summaries = pd.concat([az.summary(data1, var_names=['mu', 'tau']),
                           az.summary(data2, var_names=['mu', 'tau']) ])
    summaries.index = ['centered_eight_mu', 'centered_eight_tau', 
                       'non_centered_eight_mu', 'non_centered_eight_tau']
    print(summaries)

    az.plot_autocorr(data1, var_names=['mu', 'tau'])
    az.plot_autocorr(data2, var_names=['mu', 'tau'])
    plt.show()

    print(data1.diverging.sum())

    _, ax = plt.subplots(1, 2, sharey=True, sharex=True, 
                         figsize=(10, 5), constrained_layout=True)

    for idx, tr in enumerate([data1, data2]):
        az.plot_pair(tr, var_names=['mu', 'tau'], 
                     kind='scatter', divergences=True, divergences_kwargs={'color':'C1'},
        ax=ax[idx])

        ax[idx].set_title(['centered', 'non-centered'][idx])

    plt.show()