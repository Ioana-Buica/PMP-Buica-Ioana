import pandas as pd
import numpy as np
import pymc3 as pm
from scipy import stats
import random

print(1-stats.poisson.cdf(50, mu=20))

nr_case_marcat  = 1
nr_statie_gatit = 4

nr_mese = 26

"""
for i in range(20):  
    succes = 0

    for j_statie_gatit in range(10000):

        nr_clienti = stats.poisson.rvs(mu=20)

        t_casa  = stats.norm.rvs(loc=1, scale=0.5, size=nr_case_marcat)
        t_gatit = stats.expon.rvs(scale=2, size=nr_statie_gatit)
        t_masa  = stats.norm.rvs(loc=10, scale=2, size=nr_mese)

        t_asteptare = []

        if nr_case_marcat >= nr_clienti and nr_statie_gatit >= nr_clienti:
            for i in range(nr_clienti):
                num_asteptare = t_casa[i] + t_gatit[i]
                t_asteptare.append(num_asteptare)

        elif nr_case_marcat >= nr_clienti: # nr_statie_gatit < nr_clienti
            for i in range(nr_statie_gatit):
                num_asteptare = t_casa[i] + t_gatit[i]
                t_asteptare.append(num_asteptare)

            for i in range(nr_statie_gatit,nr_clienti):
                minn = min(t_gatit)
                num = random.choice(t_gatit)

                num_asteptare = t_casa[i] + num + minn
                t_asteptare.append(num_asteptare)

        elif nr_statie_gatit >= nr_clienti: # nr_case_marcat < nr_clienti
            for i in range(nr_case_marcat):
                num_asteptare = t_casa[i] + t_gatit[i]
                t_asteptare.append(num_asteptare)

            for i in range(nr_case_marcat,nr_clienti):
                minn = min(t_casa)
                num = random.choice(t_casa)

                num_asteptare = t_gatit[i] + num + minn
                t_asteptare.append(num_asteptare)

        else: # nr_case_marcat < nr_clienti and nr_statie_gatit < nr_clienti
            if nr_case_marcat > nr_statie_gatit:
                for i in range(nr_statie_gatit):
                    num_asteptare = t_casa[i] + t_gatit[i]
                    t_asteptare.append(num_asteptare)

                for i in range(nr_statie_gatit,nr_case_marcat):
                    minn = min(t_gatit)
                    num = random.choice(t_gatit)

                    num_asteptare = t_casa[i] + num + minn
                    t_asteptare.append(num_asteptare)

                for i in range(nr_case_marcat,nr_clienti):
                    minn = min(t_asteptare)
                    num_gatit = random.choice(t_gatit)
                    num_casa = random.choice(t_casa)

                    num_asteptare = minn + num_casa + num_gatit
                    t_asteptare.append(num_asteptare)

            else: # nr_case_marcat <= nr_statie_gatit
                for i in range(nr_case_marcat):
                    num_asteptare = t_casa[i] + t_gatit[i]
                    t_asteptare.append(num_asteptare)

                for i in range(nr_case_marcat,nr_statie_gatit):
                    minn = min(t_casa)
                    num = random.choice(t_casa)

                    num_asteptare = t_gatit[i] + num + minn
                    t_asteptare.append(num_asteptare)

                for i in range(nr_statie_gatit,nr_clienti):
                    minn = min(t_asteptare)
                    num_gatit = random.choice(t_gatit)
                    num_casa = random.choice(t_casa)

                    num_asteptare = minn + num_casa + num_gatit
                    t_asteptare.append(num_asteptare)
        
        succes += 1

        for i in range(len(t_asteptare)):
            if t_asteptare[i] >= 15:
                succes -= 1

    prob = succes/10000

    print(nr_case_marcat, nr_statie_gatit, prob)

    if prob>0.95:
        nr_statie_gatit = nr_statie_gatit - 1
    else: nr_statie_gatit = nr_statie_gatit + 1

for i in range(20):  
    succes = 0

    for j_statie_gatit in range(10000):

        nr_clienti = stats.poisson.rvs(mu=20)

        t_casa  = stats.norm.rvs(loc=1, scale=0.5, size=nr_case_marcat)
        t_gatit = stats.expon.rvs(scale=2, size=nr_statie_gatit)
        t_masa  = stats.norm.rvs(loc=10, scale=2, size=nr_mese)

        t_asteptare = []

        if nr_case_marcat >= nr_clienti and nr_statie_gatit >= nr_clienti:
            for i in range(nr_clienti):
                num_asteptare = t_casa[i] + t_gatit[i]
                t_asteptare.append(num_asteptare)

        elif nr_case_marcat >= nr_clienti: # nr_statie_gatit < nr_clienti
            for i in range(nr_statie_gatit):
                num_asteptare = t_casa[i] + t_gatit[i]
                t_asteptare.append(num_asteptare)

            for i in range(nr_statie_gatit,nr_clienti):
                minn = min(t_gatit)
                num = random.choice(t_gatit)

                num_asteptare = t_casa[i] + num + minn
                t_asteptare.append(num_asteptare)

        elif nr_statie_gatit >= nr_clienti: # nr_case_marcat < nr_clienti
            for i in range(nr_case_marcat):
                num_asteptare = t_casa[i] + t_gatit[i]
                t_asteptare.append(num_asteptare)

            for i in range(nr_case_marcat,nr_clienti):
                minn = min(t_casa)
                num = random.choice(t_casa)

                num_asteptare = t_gatit[i] + num + minn
                t_asteptare.append(num_asteptare)

        else: # nr_case_marcat < nr_clienti and nr_statie_gatit < nr_clienti
            if nr_case_marcat > nr_statie_gatit:
                for i in range(nr_statie_gatit):
                    num_asteptare = t_casa[i] + t_gatit[i]
                    t_asteptare.append(num_asteptare)

                for i in range(nr_statie_gatit,nr_case_marcat):
                    minn = min(t_gatit)
                    num = random.choice(t_gatit)

                    num_asteptare = t_casa[i] + num + minn
                    t_asteptare.append(num_asteptare)

                for i in range(nr_case_marcat,nr_clienti):
                    minn = min(t_asteptare)
                    num_gatit = random.choice(t_gatit)
                    num_casa = random.choice(t_casa)

                    num_asteptare = minn + num_casa + num_gatit
                    t_asteptare.append(num_asteptare)

            else: # nr_case_marcat <= nr_statie_gatit
                for i in range(nr_case_marcat):
                    num_asteptare = t_casa[i] + t_gatit[i]
                    t_asteptare.append(num_asteptare)

                for i in range(nr_case_marcat,nr_statie_gatit):
                    minn = min(t_casa)
                    num = random.choice(t_casa)

                    num_asteptare = t_gatit[i] + num + minn
                    t_asteptare.append(num_asteptare)

                for i in range(nr_statie_gatit,nr_clienti):
                    minn = min(t_asteptare)
                    num_gatit = random.choice(t_gatit)
                    num_casa = random.choice(t_casa)

                    num_asteptare = minn + num_casa + num_gatit
                    t_asteptare.append(num_asteptare)
        
        succes += 1

        for i in range(len(t_asteptare)):
            if t_asteptare[i] >= 15:
                succes -= 1

    prob = succes/10000

    print(nr_case_marcat, nr_statie_gatit, prob)

    if prob>0.95:
        nr_case_marcat = nr_case_marcat - 1
    else: nr_case_marcat = nr_case_marcat + 1
"""
for i in range(20):  
    succes = 0

    for j_statie_gatit in range(10000):

        nr_clienti = stats.poisson.rvs(mu=20)

        t_casa  = stats.norm.rvs(loc=1, scale=0.5, size=nr_case_marcat)
        t_gatit = stats.expon.rvs(scale=2, size=nr_statie_gatit)
        t_masa  = stats.norm.rvs(loc=10, scale=2, size=nr_mese)

        if nr_clienti <= nr_mese:
            succes += 1

    prob = succes/10000

    if prob>0.90:
        nr_mese = nr_mese - 1
    else: nr_mese = nr_mese + 1

 
print("\n\n\n")
print(nr_mese)