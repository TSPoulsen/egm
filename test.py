from scipy.stats import chi2
from chi2comb import chi2comb_cdf, ChiSquared
import numpy as np
import matplotlib.pyplot as plt
import random
import math

prod_table = {}


def edf(x, sigmas):
    total = 0
    for i, sig in enumerate(sigmas):
        top = math.exp(-x/(sig**2))
        bot = sig**2
        for j, sig2 in enumerate(sigmas):
            if j == i: continue
            bot *= (1 - (sig2**2)/(sig**2))
        total += top / bot
    return total

def cdf(x, sigmas, prod_table):
    total = 0
    for i, sig in enumerate(sigmas):
        top = math.exp(-x/(sig**2))
        total += top / prod_table[i]
    return -total + 1



d = 10 
samples = 10000
sigmas = np.array([random.random() * 10 + 1 for _ in range(d)])
means = np.zeros((d))

for i, sig in enumerate(sigmas):
    bot = 1
    for j, sig2 in enumerate(sigmas):
        if j == i: continue
        bot *= (1 - (sig2**2)/(sig**2))
    prod_table[i] = bot
print(prod_table)
random_vec = np.random.normal(means, sigmas, size=(samples, d))
ips = np.sum(random_vec * random_vec, axis=1)
xs = np.arange(0,1000,0.1)
#theory_ips = np.array([edf(x,sigmas) for x in xs])
cdf_y = np.array([cdf(x,sigmas, prod_table) for x in xs])
chi2s = [ChiSquared(sigmas[i]**2, 0, 1) for i in range(d)]
theory_ips2 = np.array([chi2comb_cdf(x,chi2s,0, lim = 50000)[0] for x in xs])
plt.plot(xs, theory_ips2, color = "r", label="Software package")




plt.plot(xs, cdf_y, label="Stackexchange function")
plt.hist(
    ips,
    bins = 100,
    cumulative=True,
    density=True,
    label="Emperical Data",
    histtype="step",
    alpha=0.8,
    color="k",
)
plt.xlabel("Squared norm $\|x \|^2$")
plt.ylabel("Cumulative Distribution")
plt.xlim(0,1000)
plt.legend()
plt.show()
