from time import perf_counter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymc3 as pm
import arviz as az

if __name__ == '__main__':

    model = pm.Model()

    with model:
        cutremur = pm.Bernoulli('U', 0.0005) # 0,05%
        incendiu = pm.Bernoulli('R', 0.01)  # 1%         
                                   
                                           # pm.math.switch(TRUE, FALSE)                  #    95%   98%                        #    0,01%   2% 
        activare_p = pm.Deterministic('C_p', pm.math.switch(incendiu, pm.math.switch(cutremur, 0.95, 0.98), pm.math.switch(cutremur, 0.0001, 0.02)))
                                                                      # incendiu == true                     # incendiu == false

        
        activare = pm.Bernoulli('T', p=activare_p)
        trace = pm.sample(20000)

    # se poate folosi si FOR(...)
    dictionary = {
            'cutremur': trace['U'].tolist(),
            'incendiu': trace['R'].tolist(),
            'activare': trace['T'].tolist()
            }
                
    df = pd.DataFrame(dictionary)

    p_cutremur = df[((df['cutremur'] == 1) & (df['activare'] == 1))].shape[0] / df[df['activare'] == 1].shape[0]

    p_incendiu = df[((df['incendiu'] == 1) & (df['activare'] == 0))].shape[0] / df[df['activare'] == 0].shape[0]

    print(p_cutremur)
    print(p_incendiu)

    #freeze_support()

