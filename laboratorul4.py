from time import perf_counter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymc3 as pm
import arviz as az

if __name__ == '__main__':

    model = pm.Model()
    #for x in range(1,15):

    α = 10
    with model:
                            #  clienti pe minut 1/3
        clienti     = pm.Poisson("C", 20/60)
        BoundedNormal = pm.Bound(pm.Normal, lower=0.0)
                                    #  mean, Standard deviation
        timp        = BoundedNormal("T",   1,    0.5)
        
        statieGatit = pm.Exponential("SG", α)
        trace = pm.sample(20000)

    dictionary = {
            'clienti': trace['C'].tolist(),
            'timp': trace['T'].tolist(),
            'statieGatit': trace['SG'].tolist()
            }
                
    df = pd.DataFrame(dictionary)

    #p_servire = df[((df['clienti'] == 1) & (df['statieGatit'] == 1))].shape[0] / df[df['clienti'] == 1].shape[0]
    #print(p_servire)
