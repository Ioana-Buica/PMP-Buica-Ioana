from time import perf_counter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymc3 as pm
import arviz as az

if __name__ == '__main__':

    model = pm.Model()

    with model:
                            #  clienti pe minut 1/3
                            #  clienti pe ora
        clienti     = pm.Poisson("C", 20)
        BoundedNormal = pm.Bound(pm.Normal, lower=0.0)
                                    #   mean, Standard deviation
        timp        = BoundedNormal("T",   1,    0.5)

        α = 0.15 # -> prin incercari
        BoundedExponential = pm.Bound(pm.Exponential, lower=0.0)
        statieGatit = pm.Exponential("SG", α)

        timpServire = BoundedNormal("TS",mu=statieGatit, sd=timp )
        #az.plot_posterior({'a':clienti})
        trace = pm.sample(1000) #, return_inferencedata=True)
    #az.plot_trace(trace)

    dictionary = {
            #'clienti': trace['C'].tolist(),
            #'timp': trace['T'].tolist(),
            #'statieGatit': trace['SG'].tolist(),
            'timpServire': trace['TS'].tolist()
            }
                
    df = pd.DataFrame(dictionary)

    p_servire = df[(df['timpServire'] < 15)].shape[0] / df.shape[0]
    print(p_servire)
    print(df['timpServire'].mean())
    print(df['timpServire'].max())
