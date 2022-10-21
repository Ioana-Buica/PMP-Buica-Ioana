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
        clienti     = pm.Poisson("clienti", 20/60)
                                    #  mean, Standard deviation
        timp        = pm.Normal("timp",   1,    0.5)
        α = 10
        statieGatit = pm.Exponential("statie_de_gatit", α)
        trace = pm.sample(20000)

    dictionary = {
            'clienti': trace['C'].tolist(),
            'timp': trace['T'].tolist(),
            'statieGatit': trace['SG'].tolist()
            }
                
    df = pd.DataFrame(dictionary)