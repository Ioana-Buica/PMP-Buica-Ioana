import numpy as np
from scipy import stats
import pymc3 as pm

import matplotlib.pyplot as plt
import arviz as az

def posterior_grid(grid_points, heads, tails):
    """
    A grid implementation for the coin-flipping problem
    """
    grid = np.linspace(0, 1, grid_points)
    prior = abs(grid - 0.5)

    likelihood = stats.binom.pmf(heads, heads+tails, grid)

    posterior = likelihood * prior
    posterior /= posterior.sum()

    return grid, posterior

def estimati_pi(N):
    # N = 10000
    x, y = np.random.uniform(-1, 1, size=(2, N))
    inside = (x**2 + y**2) <= 1
    outside = np.invert(inside)

    pi = inside.sum()*4/N

    error = abs((pi - np.pi) / pi) * 100
    # error = (N - inside.sum()) / N
    # error = outside.sum()/N
    
    """plt.figure(figsize=(8, 8))
    plt.plot(x[inside], y[inside], 'b.')
    plt.plot(x[outside], y[outside], 'r.')
    plt.plot(0, 0, label=f'π*= {pi:4.3f}\n error = {error:4.3f}', alpha=0)
    plt.axis('square')
    plt.xticks([])
    plt.yticks([])
    plt.legend(loc=1, frameon=True, framealpha=0.9)

    #plt.show()
    plt.close()"""

    return error

def metropolis(func, draws=10000):
    """A very simple Metropolis implementation"""

    trace = np.zeros(draws)
    old_x = 0.5 # func.mean()
    old_prob = func.pdf(old_x)
    delta = np.random.normal(0, 0.5, draws)

    for i in range(draws):
        new_x = old_x + delta[i]
        new_prob = func.pdf(new_x)
        acceptance = new_prob / old_prob

        if acceptance >= np.random.random():
            trace[i] = new_x
            old_x = new_x
            old_prob = new_prob
        else:
            trace[i] = old_x
    return trace

if __name__ == '__main__':

    # Sa presupunem ca am aruncat de 100 ori o moneda  ̧
    # si am observat 58 de steme
    """data = np.repeat([0, 1], (42, 58))
    points = 10
    h = data.sum()
    t = len(data) - h
    grid, posterior = posterior_grid(points, h, t)
    plt.plot(grid, posterior, 'o-')
    plt.title(f'heads = {h}, tails = {t}')
    plt.yticks([])
    plt.xlabel('θ')

    plt.savefig('ex1.png')
    plt.close()"""

    """i = 100
    media = 0
    deviatia = 0
    nr = 0
    while i <= 10000:
        for j in range(0,10):

            x = i
            y = estimati_pi(i)

            plt.errorbar(x, y, xerr=0.1, yerr=0.1)

            media = media + y
            nr = nr + 1

        i = i + 100

    print("media: ", media)
    print("deviatia standard: ", media/nr)

    plt.savefig('ex2.png')
    plt.close()
    
    list_erors = []
    list_erors.append(estimati_pi(100))
    list_erors.append(estimati_pi(1000))
    list_erors.append(estimati_pi(10000))

    print("media: ", np.mean(list_erors))
    print("deviatia standard: ", np.std(list_erors))
    """

    n_trials = [0, 1, 2, 3, 4, 8, 16, 32, 50, 150]
    data = [0, 1, 1, 1, 1, 4, 6, 9, 13, 48]

    beta_params = [(1, 1), (20, 20), (1, 4)]
    dist = stats.beta(2,5)
    x = np.linspace(0, 1, 200)
    for idx, N in enumerate(n_trials):

        y = data[idx]

        for (a_prior, b_prior) in beta_params:
            func = stats.beta(a_prior + y, b_prior + N - y)
            # func = stats.beta(2, 5)

            trace = metropolis(func=func)
            x = np.linspace(0.01, .99, 100)
            y = func.pdf(x)
            y = func
            plt.xlim(0, 1)
            plt.plot(x, y, 'C1-', lw=3, label='True distribution')
            plt.hist(trace[trace > 0], bins=25, density=True, label='Estimated distribution')
            plt.xlabel('x')
            plt.ylabel('pdf(x)')
            plt.yticks([])
            #plt.legend()

            grid, posterior = posterior_grid(x, a_prior + y, b_prior + N - y)
            plt.plot(grid, posterior, 'o-')
            plt.title(f'heads = {a_prior + y}, tails = {b_prior + N - y}')
            plt.yticks([])
            plt.xlabel('θ')

    plt.savefig('ex3.png')
    plt.close()

