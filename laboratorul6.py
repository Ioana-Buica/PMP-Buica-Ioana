"""
import csv

with open("./data.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
    print(row[3])
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymc3 as pm
import arviz as az

headers = ['', 'ppvt', 'educ_cat', 'momage']
df = pd.read_csv('data.csv', names=headers)

df['ppvt'] = pd.to_numeric(df['ppvt'],errors='coerce')
df['educ_cat'] = pd.to_numeric(df['educ_cat'],errors='coerce')
df['momage'] = pd.to_numeric(df['momage'],errors='coerce')

#print(df.dtypes)
#print(df)

X = df['ppvt']
Y = df['momage']

plt.scatter(X, Y,  color='black')
#plt.plot(X, Y, 'C0.')
plt.xlabel('ppvt',)
plt.ylabel('momage')
plt.xticks(())
plt.yticks(())

plt.show()

X = df['ppvt'].fillna(0.0).astype(int).values
Y = df['momage'].fillna(0.0).astype(int).values

"""if __name__ == '__main__':

    model = pm.Model()

    with pm.Model() as model_g:
        α = pm.Normal('α', mu=0, sd=10)
        β = pm.Normal('β', mu=0, sd=1)
        ε = pm.HalfCauchy('ε', 5)
        μ = pm.Deterministic('μ', α + β * X)
        y_pred = pm.Normal('y_pred', mu=μ, sd=ε, observed=Y)

        idata_g = pm.sample(20, tune=20, return_inferencedata=True)

    az.plot_trace(idata_g, var_names=['α','β','ε'])"""







